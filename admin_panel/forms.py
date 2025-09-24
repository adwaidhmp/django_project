from django import forms
from student_management.models import CustomUser
from student_management.models import Department
class FullCustomUserChangeForm(forms.ModelForm):
    class Meta:
        password = None  # Hide password field
        model = CustomUser
        fields = ['username','roll_number','department','year_of_admission','date_of_birth', 'email',
                  'age', 'place', 'phone','profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'year_of_admission': forms.NumberInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'roll_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use by another student.")
        return email

    # Validation for roll number
    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        qs = CustomUser.objects.exclude(pk=self.instance.pk).filter(roll_number=roll_number)
        if qs.exists():
            raise forms.ValidationError("This roll number is already assigned to another student.")
        return roll_number


