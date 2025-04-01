from django import forms
from .models import item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator,MinValueValidator
import re


class AdForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ('product_title', 'category', 'product_description', 'price', 'location',
                  'seller_phone', 'image1', 'image2')
        exclude = ['seller']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Eircode validation to the location field
        self.fields['location'].validators.append(
            RegexValidator(
                regex=r'^[A-Za-z]{1}[0-9]{2}[A-Za-z]{2}[0-9]{2}$',
                message="Enter a valid Eircode (e.g., D12YR86)."
            )
        )

        # Add price validation to ensure only numbers are entered
        self.fields['price'].validators.append(
            RegexValidator(
                regex=r'^\d+(\.\d{1,2})?$',  # Allows integers or decimals with up to 2 decimal places
                message="Enter a valid price (numbers only)."
            )
        )
        self.fields['price'].validators.append(
            MinValueValidator(0, message="Price must be a positive number.")
        )

class CustomUserCreationForm(UserCreationForm): 
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email
    
    def clean_password1(self):  
        password1 = self.cleaned_data.get('password1')

        # length validation
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Uppercase and lowercase validation
        if not any(char.isupper() for char in password1) or not any(char.islower() for char in password1):
            raise ValidationError("Password must contain both uppercase and lowercase letters.")

        # Special character validation
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("Password must contain at least one special character.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
    
    
