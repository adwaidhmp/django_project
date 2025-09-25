from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from .models import CustomUser, Department


# Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    place = forms.CharField(required=True)
    phone = forms.CharField(required=True, max_length=15)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")
    date_of_birth = forms.DateField(required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False)
    class Meta: 
        model = CustomUser
        fields = [
            'profile_picture','username', 'email','date_of_birth', 'age', 'place',
            'phone', 'department','password1', 'password2',
        ] #give orderly how yo want

        
# Login Form
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


# updation form
class CustomUserChangeForm(UserChangeForm):
    password = None  # Hide password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'place', 'phone', 'date_of_birth']  # Added date_of_birth
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' }),
            }

    def clean_email(self): 
        email = self.cleaned_data.get('email') 
        qs = CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.") #form field errros
        return username