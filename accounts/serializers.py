from rest_framework import serializers
from .models import CustomUser, Subject, StudentMarks

# --- 1. USER SERIALIZER ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Added 'id' here so the frontend can identify users!
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# --- 2. SUBJECT SERIALIZER ---
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']

# --- 3. MARKS SERIALIZER ---
class StudentMarksSerializer(serializers.ModelSerializer):
    # These fields explicitly fetch the text names (e.g., "Mathematics")
    # instead of just the ID numbers.
    student_name = serializers.ReadOnlyField(source='student.username')
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = StudentMarks
        fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 'marks_obtained', 'total_marks']