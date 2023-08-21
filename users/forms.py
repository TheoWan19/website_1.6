from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from . models import Profile, CustomUser


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(help_text='A valid email address, please.', required=True)
	password1 = forms.CharField(label='Password', help_text='Enter Your Password', widget=forms.PasswordInput())

	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()

		return user		


class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)

	username = forms.CharField(widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder':'Username Or Email'}),
		label='Username Or Email*')		

	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder':'Enter Your Password'}))	

	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = CustomUser()
		fields = ['first_name', 'last_name', 'email', 'mobile', 'date_birth', 'gender','description']	