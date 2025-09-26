from django.shortcuts import render
from student_management.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from student_management.forms import CustomUserCreationForm
from .forms import FullCustomUserChangeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from student_management.models import Department,AddOnCourse,CoursePurchaseRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone



@login_required
def std_view(request):
    query = request.GET.get('q', '')  # Get search query
    gender_filter = request.GET.get('gender', '')
    
    students = CustomUser.objects.all().order_by('roll_number')
    
    if query:
        students = students.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(department__name__icontains=query)
        )
        
    if gender_filter:
        students = students.filter(gender=gender_filter)

    # Pagination: 10 students per page
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'query': query,
        'gender_filter': gender_filter,
    }
    return render(request, 'student_view.html', context)


@login_required
def std_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST ,request.FILES)
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
def std_delete(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('std_view')

@login_required
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
def edit_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == "POST":
        dept.name = request.POST.get("name")
        dept.save()
        messages.success(request, "Department updated successfully!")
        return redirect("department")
    
@login_required
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    if request.method == "POST":
        dept.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect("department")

#course managae(add,edit,delete)   
@login_required
def course_manage(request):
    if request.method == "POST":
        course = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        if course:
            if AddOnCourse.objects.filter(course=course).exists():
                messages.error(request, "Course with this name already exists.")
            else:
                AddOnCourse.objects.create(
                    course=course,
                    description=description,
                    price=price
                )
                messages.success(request, "Course added successfully!")
                return redirect("course_manage")
        else:
            messages.error(request, "Course course cannot be empty.")

    courses = AddOnCourse.objects.all().order_by('id')
    return render(request, "addoncourse.html", {"courses": courses})


@login_required
def course_edit(request, course_id):
    course = get_object_or_404(AddOnCourse, id=course_id)
    if request.method == "POST":
        course.course = request.POST.get("course")
        course.description = request.POST.get("description")
        course.price = request.POST.get("price")
        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect("course_manage")


@login_required
def course_delete(request, course_id):
    course = get_object_or_404(AddOnCourse, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect("course_manage")

#notif
@login_required
def manage_course_requests(request):
    requests = CoursePurchaseRequest.objects.filter(status='pending')
    return render(request, 'manage_course.html', {'requests': requests})

# Approve request
@login_required
def approve_request(request, request_id):
    purchase_request = get_object_or_404(CoursePurchaseRequest, id=request_id)
    purchase_request.status = 'approved'
    purchase_request.approved_at = timezone.now()
    purchase_request.save()

    # Add course to student purchased_courses
    purchase_request.student.purchased_courses.add(purchase_request.course)
    # Send email notification
    subject = f'Course Approved: {purchase_request.course.course}'
    message = f'Hello {purchase_request.student.username},\n\n' \
              f'Your purchase request for the course "{purchase_request.course.course}" has been approved.\n' \
              f'You can now access the course in your profile.\n\n' \
              'Happy Learning!\nStudent Management Team'
    recipient = [purchase_request.student.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False)
    
    messages.success(request, f'Course "{purchase_request.course.course}" approved for {purchase_request.student.username}.')
    return redirect('manage_course_requests')

# Reject request
@login_required
def reject_request(request, request_id):
    purchase_request = get_object_or_404(CoursePurchaseRequest, id=request_id)
    purchase_request.status = 'rejected'
    purchase_request.save()
    messages.success(request, f'Course "{purchase_request.course.course}" rejected for {purchase_request.student.username}.')
    return redirect('manage_course_requests')