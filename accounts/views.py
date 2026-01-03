from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

# Import Models & Serializers
from .models import CustomUser, SystemSettings, Subject, StudentMarks
from .serializers import UserSerializer, SubjectSerializer, StudentMarksSerializer

# --- 1. REGISTER USER ---
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 2. LOGIN USER ---
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        settings, _ = SystemSettings.objects.get_or_create(id=1)
        
        return Response({
            'message': 'Login Successful!',
            'username': user.username,
            'role': getattr(user, 'role', 'Student'),
            'permissions': {
                'grading_allowed': settings.grading_allowed,
                'results_published': settings.results_published
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Username or Password'}, status=status.HTTP_401_UNAUTHORIZED)

# --- 3. UPDATE USER ROLE (Principal) ---
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_role(request, username):
    if getattr(request.user, 'role', '') != 'Principal':
        return Response({'error': 'Unauthorized'}, status=403)

    user_to_update = get_object_or_404(CustomUser, username=username)
    new_role = request.data.get('role')
    
    valid_roles = ['Principal', 'Teacher', 'Student']
    if new_role not in valid_roles:
        return Response({'error': f'Invalid role. Choose: {valid_roles}'}, status=400)

    user_to_update.role = new_role
    user_to_update.save()
    return Response({'message': f'User {username} is now a {new_role}'}, status=200)

# --- 4. TOGGLE SETTINGS (Principal) ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_settings(request):
    if getattr(request.user, 'role', '') != 'Principal':
        return Response({'error': 'Unauthorized'}, status=403)

    settings, _ = SystemSettings.objects.get_or_create(id=1)
    
    if 'grading_allowed' in request.data:
        settings.grading_allowed = request.data['grading_allowed']
    if 'results_published' in request.data:
        settings.results_published = request.data['results_published']
    
    settings.save()
    return Response({'message': 'System settings updated'}, status=200)

# --- 5. GET SETTINGS (Public) ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_system_settings(request):
    settings, _ = SystemSettings.objects.get_or_create(id=1)
    return Response({
        'grading_allowed': settings.grading_allowed,
        'results_published': settings.results_published
    }, status=200)

# --- 6. GET SUBJECTS (Dynamic) ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_subjects(request):
    # If user is logged in and is a Teacher, show ONLY their assigned subjects
    if request.user.is_authenticated and request.user.role == 'Teacher':
        subjects = request.user.subjects.all()
    else:
        # Principals, Students, or Guests see ALL subjects
        subjects = Subject.objects.all()
        
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

# --- 7. GET STUDENTS ---
@api_view(['GET'])
@permission_classes([AllowAny])  
def get_students(request):
    students = CustomUser.objects.filter(role='Student')
    serializer = UserSerializer(students, many=True)
    return Response(serializer.data)

# --- 8. GET TEACHERS STATUS (For Principal Table) ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_teachers_status(request):
    teachers = CustomUser.objects.filter(role='Teacher')
    data = []
    for t in teachers:
        # Serialize the list of subjects assigned to this teacher
        subject_data = SubjectSerializer(t.subjects.all(), many=True).data
        data.append({
            'id': t.id,
            'username': t.username,
            'subjects': subject_data
        })
    return Response(data)

# --- 9. UPDATE TEACHER SUBJECTS (Principal Action) ---
@api_view(['POST'])
@permission_classes([AllowAny]) 
def update_teacher_subjects(request):
    # Retrieve data from frontend
    teacher_id = request.data.get('teacher_id')
    subject_ids = request.data.get('subject_ids') # Expecting list: [1, 2]

    try:
        teacher = CustomUser.objects.get(id=teacher_id)
        
        # 1. Clear old subjects
        teacher.subjects.clear()
        
        # 2. Add new subjects based on IDs sent
        if subject_ids:
            for sub_id in subject_ids:
                try:
                    subject = Subject.objects.get(id=sub_id)
                    teacher.subjects.add(subject)
                except Subject.DoesNotExist:
                    pass # Skip invalid IDs
            
        return Response({'status': 'success', 'message': f'Subjects updated for {teacher.username}'})
    except CustomUser.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# --- 10. ADD MARKS (With Subject Check) ---
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def add_marks(request):
    data = request.data
    
    # Security: Verify Teacher owns this subject
    if request.user.is_authenticated and request.user.role == 'Teacher':
        try:
            sub_id_check = int(data.get('subject_id'))
            if not request.user.subjects.filter(pk=sub_id_check).exists():
                return Response({'error': '⛔ You are not authorized to grade this subject!'}, status=403)
        except:
            pass # If ID invalid, it will fail below anyway

    try:
        # 1. Get Student
        student_id = data.get('student_id')
        if str(student_id).isdigit():
            s_obj = CustomUser.objects.get(pk=student_id)
        else:
            s_obj = CustomUser.objects.get(username=student_id)

        # 2. Get Subject
        subject_id = data.get('subject_id')
        if str(subject_id).isdigit():
            sub_obj = Subject.objects.get(pk=subject_id)
        else:
            sub_obj = Subject.objects.get(name=subject_id)

        # 3. Save Marks
        marks_val = int(data['marks'])
        
        StudentMarks.objects.update_or_create(
            student=s_obj,
            subject=sub_obj,
            defaults={'marks_obtained': marks_val}
        )
        return Response({'message': '✅ Marks saved successfully!'}, status=200)

    except CustomUser.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# --- 11. GET MY MARKS (Cheat Mode / Student View) ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_my_marks(request):
    try:
        # For testing, we force 'student1' if user not logged in
        if request.user.is_authenticated:
            target_user = request.user
        else:
            target_user = CustomUser.objects.get(username='student1')
            
        marks = StudentMarks.objects.filter(student=target_user)
        serializer = StudentMarksSerializer(marks, many=True)
        return Response(serializer.data)
        
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)