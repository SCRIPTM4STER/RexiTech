from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

        # Set help_text to None for all fields
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        # Explicitly add class for password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['username'].help_text = None
        self.fields['password'].help_text = None





class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)  # Add username field here

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        # Pop the user instance from the keyword arguments, if present
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Set the initial username value from the User model
        if self.user:
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        # Save the UserProfile instance
        profile = super(EditProfileForm, self).save(commit=False)
        if commit:
            profile.save()
        
        # Save the User's username
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.save()
        
        return profile