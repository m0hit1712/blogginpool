from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TempUserMessage)
admin.site.register(UserClone)
