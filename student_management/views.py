from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm,CustomUserChangeForm
from django.core.mail import send_mail
from django.conf import settings
from student_management.models import AddOnCourse
from django.shortcuts import get_object_or_404
from .models import CoursePurchaseRequest
from django.utils import timezone
# Home View

def home_view(request):
    return render(request, 'base.html')  

# Registration View

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) # Include request.FILES to get profile picture
        if form.is_valid():
            student = form.save()
            #email sending
            subject = "Welcome to ABC College"
            message = f"Hi {student.username},\n\nWelcome! Your account has been successfully created."
            recipient = student.email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser or user.is_staff:
                messages.error(request, 'Admins cannot log in here. Please use the admin panel.')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_superuser:
                return redirect('/adm/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout View

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# Profile View

@login_required()
def profile_view(request):
    user = request.user #Where request.user comes from Django attaches the user attribute to every HttpRequest object via middleware.
    courses = AddOnCourse.objects.all()
    pending_requests = CoursePurchaseRequest.objects.filter(student=user, status='pending')
    approved_requests = CoursePurchaseRequest.objects.filter(student=user, status='approved')
    completed_requests = CoursePurchaseRequest.objects.filter(student=user, status='completed')
    rejected_requests = CoursePurchaseRequest.objects.filter(student=user, status='rejected')
    context = {
        'user': user,
        'courses': courses,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'completed_requests': completed_requests,
        'rejected_requests': rejected_requests,
    }
    if not user.is_authenticated:
        messages.error(request, 'You must login to view your profile.')
        return redirect('login') 
    return render(request, 'profile.html', context)


#edit profile view

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=request.user) 

    return render(request, 'edit_profile.html', {'form': form})



@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(AddOnCourse, id=course_id)
    # Check if already purchased
    if request.user.purchased_courses.filter(id=course.id).exists():
        messages.info(request, f'You already own "{course.course}".')
        return redirect('profile')
    # Check if there is already a pending request
    if CoursePurchaseRequest.objects.filter(student=request.user, course=course, status='pending').exists():
        messages.info(request, f'Your purchase request for "{course.course}" is already pending.')
        return redirect('profile')
    # Create a pending purchase request
    CoursePurchaseRequest.objects.create(student=request.user, course=course)
    messages.success(request, f'Your purchase request for "{course.course}" has been submitted and is pending approval.')
    return redirect('profile')

@login_required
def mark_course_completed(request, course_id):
    purchase_request = get_object_or_404(
        CoursePurchaseRequest,
        student=request.user,
        course_id=course_id,
        status='approved'  # Only "In Progress" courses can be marked completed
    )

    purchase_request.status = 'completed'
    purchase_request.completed_at = timezone.now()
    purchase_request.save()

    messages.success(request, f'Course "{purchase_request.course.course}" marked as completed.')
    return redirect('profile')

# form.isvalid() do this
# Step 1: Field Validation

# Checks that required fields are present (username/email, password).

# Validates types / formats (e.g., string length, email format if you customize the field).

# Runs any custom validators you added in the form.

# Step 2: Authentication

# Internally calls Django’s authentication backend (ModelBackend by default):

# Looks up the user in the database table of your AUTH_USER_MODEL.

# Checks that the user exists.

# Calls user.check_password(submitted_password) to verify the password.

# Checks that is_active=True (inactive users cannot login).

# If everything is correct → stores the user object in self.user_cache.

# Step 3: Error Handling

# If any step fails (missing fields, user doesn’t exist, wrong password, inactive user):

# form.is_valid() returns False.

# Errors are added to form.errors → can be displayed in the template.