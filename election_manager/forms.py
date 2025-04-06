from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ElectionEvent


class VoterSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class InstitutionSignUpForm(UserCreationForm):
    institution_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'institution'
        if commit:
            user.save()
        return user


class ElectionForm(forms.ModelForm):
    class Meta:
        model = ElectionEvent
        fields = ['name', 'description', 'start_time', 'end_time', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }