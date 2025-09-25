from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import datetime

def get_user_details(user_id):
    """Cache and return user details"""
    cache_key = f'user_details_{user_id}'
    user_data = cache.get(cache_key)
    
    if user_data is None:
        try:
            user = CustomUser.objects.select_related('staff').get(id=user_id)
            user_data = {
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'profile_pic': user.profile_pic.url if user.profile_pic else None
            }
            cache.set(cache_key, user_data, timeout=300)  # Cache for 5 minutes
        except CustomUser.DoesNotExist:
            return None
            
    return user_data

@cache_page(60 * 15)  # Cache for 15 minutes
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("manager_home"))
        else:
            return redirect(reverse("employee_home"))
    return render(request, 'main_app/login.html')

@require_http_methods(["POST"])
def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("manager_home"))
            else:
                return redirect(reverse("employee_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return redirect("/")

def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
@cache_page(60 * 5)  # Cache for 5 minutes
def admin_home(request):
    total_staff = cache.get('total_staff')
    if total_staff is None:
        total_staff = Staff.objects.count()
        cache.set('total_staff', total_staff, 300)  # Cache for 5 minutes

    today = datetime.datetime.now()
    page_title = "Dashboard"
    
    context = {
        "total_staff": total_staff,
        "page_title": page_title,
    }
    return render(request, "main_app/admin_template/home_content.html", context)

@login_required
@cache_page(60 * 5)
def admin_view_profile(request):
    user = request.user
    context = {
        "page_title": "View/Edit Profile",
        "user": user
    }
    return render(request, "main_app/admin_template/admin_view_profile.html", context)

@login_required
@require_http_methods(["POST"])
def admin_update_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_view_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_view_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_view_profile')

@login_required
def admin_notify_manager(request):
    manager = CustomUser.objects.filter(user_type=2)
    context = {
        "page_title": "Send Notifications To Manager",
        "allManager": manager
    }
    return render(request, "main_app/admin_template/manager_notification.html", context)

@login_required
@require_http_methods(["POST"])
def send_manager_notification(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_notify_manager')
    else:
        manager_id = request.POST.get('manager_id')
        message = request.POST.get('message')
        manager = CustomUser.objects.get(id=manager_id)
        try:
            notification = NotificationManager(manager_id=manager, message=message)
            notification.save()
            messages.success(request, "Notification sent successfully")
            return redirect('admin_notify_manager')
        except Exception as e:
            messages.error(request, f"Failed to Send Notification: {str(e)}")
            return redirect('admin_notify_manager')