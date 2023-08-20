from django.contrib import admin

from .models import CustomUser, Profile

#Mix Profile info to User info
class ProfileInline(admin.StackedInline):
	model = Profile	

class CustomUserAdmin(admin.ModelAdmin):
	model = CustomUser
	fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'date_birth', 'gender','status', 'description']
	inlines = [ProfileInline]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Profile)



