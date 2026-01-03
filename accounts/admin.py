from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SystemSettings, Subject, StudentMarks

# --- 1. DEFINE ADMIN CLASSES ---

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Update fieldsets to use 'subjects' (Plural)
    fieldsets = UserAdmin.fieldsets + (
        ('Academic Info', {'fields': ('role', 'subjects', 'can_upload')}), 
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Academic Info', {'fields': ('role', 'subjects', 'can_upload')}),
    )

    # remove 'subject' from list_display because ManyToMany fields cannot be in list_display directly
    list_display = ['username', 'email', 'role', 'can_upload', 'is_staff']
    
    # Add this to make selecting multiple subjects easier
    filter_horizontal = ('subjects',)

class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'grading_allowed', 'results_published')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'total_marks')
    list_filter = ('subject',)
    search_fields = ('student__username', 'subject__name')

# --- 2. REGISTER MODELS ---
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SystemSettings, SystemSettingsAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentMarks, MarksAdmin)