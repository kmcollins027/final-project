from django.contrib.auth.forms import PasswordResetForm
from django.forms import ModelForm, ImageField
from .models import User
from django import forms


class MyPasswordResetForm(PasswordResetForm):
    def is_valid(self):
        email = self.data["email"]
        if sum([1 for u in self.get_users(email)]) == 0:
            self.add_error(None, "Unknown email; try again")
            return False
        return super().is_valid()

class UserAccountUpdateForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'image']

class ContactForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=15) 
    last_name = forms.CharField(label="Last Name", max_length=15) 
    email = forms.EmailField(label="Email Address", max_length=25) 
    message = forms.CharField(label="Message", widget=forms.Textarea)
