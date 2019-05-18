from django.contrib import admin
from .models import profile, activities, temps 
# Register your models here.

admin.site.register(profile) 
admin.site.register(activities)
admin.site.register(temps) 