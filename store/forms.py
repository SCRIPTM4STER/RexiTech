from django import forms
from .models_product import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # Removed the 'product' field
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...',
                'style': 'resize: none;',  # Optional: Prevents resizing
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',  # Example class for Bootstrap styling
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Ensure the comment field is empty
        self.fields['comment'].initial = ''







#! auth forms
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
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['remember_me'].label = 'Remember Me'
        self.fields['username'].help_text = None
        self.fields['password'].help_text = None
        self.fields['remember_me'].help_text = None





class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)  # Add username field
    email = forms.EmailField()  # Add email field

    class Meta:
        model = UserProfile  # Assuming UserProfile is a custom profile model
        fields = ['profile_picture', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Set initial values for username and email from the User model
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        # Save the UserProfile instance
        profile = super(EditProfileForm, self).save(commit=False)
        
        # Update the User model's username and email if they were changed
        if self.user:
            if self.cleaned_data['username'] != self.user.username:
                self.user.username = self.cleaned_data['username']
            if self.cleaned_data['email'] != self.user.email:
                self.user.email = self.cleaned_data['email']
            self.user.save()  # Save changes to User model

        # Save the UserProfile model instance
        if commit:
            profile.save()
        
        return profile
    

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})