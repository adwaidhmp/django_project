from django.shortcuts import render
from student_management.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from student_management.forms import CustomUserCreationForm
from .forms import FullCustomUserChangeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from student_management.models import Department
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

def admin_required(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_required)
def std_view(request):
    query = request.GET.get('q', '')  # Get search query
    students = CustomUser.objects.all().order_by('roll_number')

    if query:
        students = students.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(department__name__icontains=query)
        )

    # Pagination: 10 students per page
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'query': query
    }
    return render(request, 'student_view.html', context)


@login_required
@user_passes_test(admin_required)
def std_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            student=form.save()
            subject = "Welcome to ABC College of Arts and Science"
            message = f"Hi {student.username},\n\nWelcome! Your account has been successfully created."
            recipient = student.email
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
            messages.success(request, 'Student added successfully!')
            return redirect('std_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'student_add.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def std_edit(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = FullCustomUserChangeForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('std_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FullCustomUserChangeForm(instance=student)
    return render(request, 'student_edit.html', {'form': form})


@login_required
@user_passes_test(admin_required)
def std_delete(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('std_view')

@login_required
@user_passes_test(admin_required)
def department_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            if Department.objects.filter(name=name).exists():
                messages.error(request, 'Department with this name already exists.')
            else:
                Department.objects.create(name=name)
                messages.success(request, 'Department added successfully!')
                return redirect('department')
        else:
            messages.error(request, 'Department name cannot be empty.')

    # Show all departments
    departments = Department.objects.all()
    return render(request, 'dept.html', {'departments': departments})

@login_required
@user_passes_test(admin_required)
def edit_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == "POST":
        dept.name = request.POST.get("name")
        dept.save()
        messages.success(request, "Department updated successfully!")
        return redirect("department")
    
@login_required
@user_passes_test(admin_required)
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == "POST":
        dept.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect("department")