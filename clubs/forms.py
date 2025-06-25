from django import forms
from .models import Club, Member
from .models import Announcement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'description')
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'club','student_class',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter approved clubs
        if 'club' in self.fields:
            self.fields['club'].queryset = Club.objects.filter(is_approved=True).order_by('name')
            self.fields['club'].empty_label = "--- Select Your Club ---"
            self.fields['club'].required = True
        
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Add custom classes to each field dynamically
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

            
class SimpleUserEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Leave blank to keep the current password."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)  # Safely hash the new password

        if commit:
            user.save()
        return user


    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user