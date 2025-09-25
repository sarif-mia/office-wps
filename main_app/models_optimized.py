from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

class CustomUser(AbstractUser):
    user_type_choices = ((1, "CEO"), (2, "Manager"), (3, "Employee"))
    user_type = models.CharField(max_length=1, choices=user_type_choices, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

    class Meta:
        indexes = [
            models.Index(fields=['user_type']),
            models.Index(fields=['email']),
        ]
        
    def save(self, *args, **kwargs):
        # Clear cache on save
        cache_key = f'user_{self.id}'
        cache.delete(cache_key)
        super().save(*args, **kwargs)

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['admin']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return self.admin.username

class Attendance(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    status = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['attendance_date']),
        ]
        unique_together = ['staff_id', 'attendance_date']

class LeaveReportStaff(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['leave_status']),
            models.Index(fields=['created_at']),
        ]

class FeedbackStaff(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['created_at']),
        ]

class NotificationStaff(models.Model):
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['created_at']),
        ]