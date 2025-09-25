from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type']
    list_filter = ['user_type', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    list_per_page = 30

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'attendance_date', 'status']
    list_filter = ['status', 'attendance_date']
    search_fields = ['staff_id__username']
    date_hierarchy = 'attendance_date'
    list_per_page = 50

class LeaveReportAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'leave_date', 'leave_message', 'leave_status']
    list_filter = ['leave_status', 'leave_date']
    search_fields = ['staff_id__username']
    date_hierarchy = 'leave_date'
    list_per_page = 50

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'feedback', 'feedback_reply', 'created_at']
    list_filter = ['created_at']
    search_fields = ['staff_id__username', 'feedback']
    date_hierarchy = 'created_at'
    list_per_page = 30

# Register with optimized admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Staff)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LeaveReportStaff, LeaveReportAdmin)
admin.site.register(FeedbackStaff, FeedbackAdmin)
admin.site.register(NotificationStaff)