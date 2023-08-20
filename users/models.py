from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
#from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	STATUS = [
		('customer', 'customer'),
		('employee', 'employee'),
	]

	email = models.EmailField(unique=True)
	mobile = PhoneNumberField(unique=True)
	date_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	status = models.CharField(max_length=10, choices=STATUS, default='customer')
	description = models.TextField('Description', max_length=200, default='', blank=True)

	def __str__(self):
		return self.username


class Profile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self", 
		related_name="followed_by", 
		symmetrical=False,
		blank=True)	
	cin = models.CharField(max_length=10, unique=True)
	nif = models.CharField(max_length=10, unique=True)
	designation = models.CharField(max_length=100)

	date_modified = models.DateTimeField(CustomUser, auto_now=True)

	def __str__(self):
		return self.user.username

#Create Profile when new user Sign up
#@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()	
		#Have the user follow themselves
		#user_profile.follows.set([instance.profile.id])
		#user_profile.save()

post_save.connect(create_profile, sender=CustomUser)

