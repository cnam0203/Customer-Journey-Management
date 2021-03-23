from django import forms
from .models import contactForm

class formContact(forms.ModelForm):
    class Meta:
        model = contactForm
        fields = ['username', 'email', 'bod']