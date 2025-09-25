from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Department model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Custom user model
class CustomUser(AbstractUser):
    #extra fields
    phone = models.CharField(max_length=15,default='0000000000')
    age = models.PositiveIntegerField(default=18)
    place = models.CharField(max_length=100,default='unknown')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    roll_number = models.BigIntegerField(unique=True,default=0)
    year_of_admission = models.PositiveIntegerField(default=date.today().year)
    date_of_birth = models.DateField(default=date(2000,1,1))  
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    #cource purchasing 
    purchased_courses = models.ManyToManyField("AddOnCourse", related_name="students", blank=True) # a student can purchase many course
    # Default flags
    is_staff = models.BooleanField(default=False)       # Students are not staff they cant get into admin
    is_superuser = models.BooleanField(default=False)   # Only superuser manually set
    
    def save(self, *args, **kwargs):
        if not self.roll_number:
            last_user = CustomUser.objects.order_by('-roll_number').first()
            self.roll_number = last_user.roll_number + 1 if last_user else 100  # if last user exist give roll+1 or 100
        super().save(*args, **kwargs)


class AddOnCourse(models.Model):
    course = models.CharField(max_length=200)  
    description = models.TextField()          
    price = models.DecimalField(max_digits=8, decimal_places=2)  

    def __str__(self):
        return self.course

class CoursePurchaseRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'In Progress'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    course = models.ForeignKey("AddOnCourse", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')  # avoid duplicate pending requests

    def __str__(self):
        return f"{self.student.username} -> {self.course.title} ({self.status})"
    
