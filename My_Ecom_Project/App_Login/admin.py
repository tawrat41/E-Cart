from django.contrib import admin
from App_Login.models import User, Profile

# Register your models here.
admin.site.site_header = "E-Cart Admin Dashboard"
admin.site.register(User)
admin.site.register(Profile)
