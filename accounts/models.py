from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. SUBJECTS ---
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

# --- 2. SYSTEM SETTINGS ---
class SystemSettings(models.Model):
    grading_allowed = models.BooleanField(default=False)
    results_published = models.BooleanField(default=False)

# --- 3. CUSTOM USER (Principal, Teacher, Student) ---
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Principal', 'Principal'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    
    # 🌟 CHANGE IS HERE: "subjects" (Plural) + ManyToManyField
    subjects = models.ManyToManyField(Subject, blank=True, related_name='teachers')

    # Permission Switch
    can_upload = models.BooleanField(default=True, help_text="Can this teacher upload marks?")

    def __str__(self):
        return f"{self.username} ({self.role})"

# --- 4. MARKS ---
class StudentMarks(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField(default=100)
    
    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"