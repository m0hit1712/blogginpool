from django.db import models

# Create your models here.
class About(models.Model):
        paragraph = models.CharField(max_length=1000)
        contact_email = models.CharField(max_length=100)
        instagram_profile = models.CharField(max_length=200, null=True)
        facebook_profile = models.CharField(max_length=200, null=True)
        profile_image = models.CharField(max_length=500, null=True)

        def __str__(self):
                return self.contact_email

class User(models.Model):
        username = models.CharField(max_length=200)
        password = models.CharField(max_length=30)
        contact_no = models.CharField(max_length=14, null=True)
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
        email = models.CharField(max_length=100, null=False, blank=False, default=None)
        email_verified = models.BooleanField(default=False, blank=False)
        about = models.OneToOneField(About, on_delete=models.CASCADE, null=True, default=None, blank=True) 
        
        def __str__(self):
                return self.username

