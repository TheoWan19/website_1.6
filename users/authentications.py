from django.contrib.auth.backends import ModelBackend
from . models import CustomUser

class AccountBackend(ModelBackend):
	def authenticate(self, **kwargs):
		email = kwargs['username']
		password = kwargs['password']
		try:
			user = CustomUser.objects.get(username=username)
			if user.check_password(password) is True:
				return user
		except CustomUser.DoesNotExist:
			return None

		def get_user(self, user_id):
			try:
				return CustomUser.objects.get(pk=user_id)
			except CustomUser.DoesNotExist:
				return None				