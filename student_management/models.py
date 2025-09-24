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
    # Default flags
    is_staff = models.BooleanField(default=False)       # Students are not staff they cant get into admin
    is_superuser = models.BooleanField(default=False)   # Only superuser manually set
    
    def save(self, *args, **kwargs):
        if not self.roll_number:
            last_user = CustomUser.objects.order_by('-roll_number').first()
            self.roll_number = last_user.roll_number + 1 if last_user else 100  # if last user exist give roll+1 or 100
        super().save(*args, **kwargs)
    
from django.db import models

class AddOnCourse(models.Model):
    title = models.CharField(max_length=200)  # Course title
    description = models.TextField()          # Detailed description
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price of the course
    created_at = models.DateTimeField(auto_now_add=True)  # When course was created
    updated_at = models.DateTimeField(auto_now=True)      # When course was last updated

    def __str__(self):
        return self.title
