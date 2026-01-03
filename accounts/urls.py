from django.urls import path
from .views import (
    register_user, 
    login_user, 
    update_user_role, 
    toggle_settings, 
    get_system_settings, 
    get_subjects, 
    get_students, 
    add_marks, 
    get_my_marks, 
    update_teacher_subjects, 
    get_teachers_status  # <--- Added this missing import
)

urlpatterns = [
    # --- Authentication ---
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),

    # --- Principal Controls ---
    path('grant-role/<str:username>/', update_user_role, name='grant-role'),
    path('get-teachers-status/', get_teachers_status, name='get-teachers-status'),      # Table Data
    path('update-teacher-subjects/', update_teacher_subjects, name='update-teacher-subjects'), # Checkboxes

    # --- System Settings ---
    path('toggle-settings/', toggle_settings, name='toggle-settings'),
    path('get-settings/', get_system_settings, name='get-settings'),

    # --- Academic Data ---
    path('get-subjects/', get_subjects, name='get-subjects'),
    path('get-students/', get_students, name='get-students'),

    # --- Marks / Grading ---
    path('add-marks/', add_marks, name='add-marks'),
    path('get-my-marks/', get_my_marks, name='get-my-marks'),
]