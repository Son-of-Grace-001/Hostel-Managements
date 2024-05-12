from django.forms import ModelChoiceField, ModelForm
from .models import Hostel, Room, Bunk, Block
# forms.py in your app

from allauth.account.forms import SignupForm
from django import forms
from .models import Faculty, Department, Gender, CustomUser, Level
from django.core.validators import FileExtensionValidator, ValidationError

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField () 
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    matric_number = forms.CharField(max_length=15, required=True)
    gender = forms.ModelChoiceField (queryset=Gender.objects.all(), empty_label="Select Gender", required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), empty_label="Select Faculty", required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label= "Select Department", required=True)
    level = forms.ModelChoiceField(queryset=Level.objects.all(), empty_label="Select Level", required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    profile_image = forms.ImageField(validators=[
    FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # 1 MB limit

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'matric_number', 'faculty', 'department', 'level', 'phone_number', 'profile_image']


    def save(self, request):
        # Call the original save method
        user = super().save(request)

        # Your additional save logic
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.matric_number = self.cleaned_data['matric_number']
        user.gender = self.cleaned_data['gender']
        user.faculty = self.cleaned_data['faculty']
        user.department = self.cleaned_data['department']
        user.profile_image = self.cleaned_data['profile_image']
        user.level = self.cleaned_data['level']
        user.phone_number = self.cleaned_data['phone_number']

        user.save()

        # Ensure the user is marked as active after saving
        user.is_active = True
        user.save()

        return user


class EditProfileForm(ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Select Gender", required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), empty_label="Select Faculty", required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department", required=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'matric_number', 'faculty', 'gender', 'department', 'level', 'phone_number']