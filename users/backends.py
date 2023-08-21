from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from . models import CustomUser


class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = CustomUser.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
		except CustomUser.DoesNotExist:
			UserModel().set_password(password)
			return
		except UserModel.MultipleObjectsReturned:
			user = CustomUser.objects.get(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()		

		if user.check_password(password) and self.user_can_authenticate(user):	
			return user