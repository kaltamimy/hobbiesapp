from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from .models import User

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2','first_name','last_name','dob','city']

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			user = User.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f"Email {email} is already in use.")

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
		except Exception as e:
			return username
		raise forms.ValidationError(f"Username {username} is already in use.")
        
class LoginUserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','password']