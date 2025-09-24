from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm,CustomUserChangeForm
from django.core.mail import send_mail
from django.conf import settings

# Home View

def home_view(request):
    return render(request, 'base.html')  # Replace with your homepage template

# Registration View

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) # Include request.FILES to handle profile picture
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

@login_required(login_url='login')
def profile_view(request):
    user = request.user #Where request.user comes from Django attaches the user attribute to every HttpRequest object via middleware.
    if not user.is_authenticated:
        messages.error(request, 'You must login to view your profile.')
        return redirect('login') 
    return render(request, 'profile.html', {'user': user})
#How it works

# When a request comes in, the middleware checks the session (cookie) to see if the user is logged in.

# If the user is logged in:

# It retrieves the user object from the database (AUTH_USER_MODEL).

# Sets request.user to the corresponding CustomUser (or default User).

# If the user is not logged in:

# request.user is set to an AnonymousUser object.

#edit profile view

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user) #instance=request.user this tell “This form is editing an existing user object, not creating a new one.”
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=request.user) #instance=request.user tells Django: “This form is bound to the existing user object.”Django automatically fills each form field with the current value from the model instance.

    return render(request, 'edit_profile.html', {'form': form})


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