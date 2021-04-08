from django.db import models

# Create your models here.

class TempUserMessage(models.Model):
        number = models.CharField(max_length=14, null=True)
        last_incoming = models.CharField(max_length=10000, default=None, null=True)
        last_outgoing = models.CharField(max_length=2000, default=None, null=True)
        datatime = models.DateTimeField(auto_now_add=True)


class UserClone(models.Model):
        username = models.CharField(max_length=200, default=None, null=True)
        password = models.CharField(max_length=30, null=True)
        contact_no = models.CharField(max_length=14, null=True)
        first_name = models.CharField(max_length=30, null=True)
        last_name = models.CharField(max_length=30, null=True)
        email = models.CharField(max_length=100, null=True, default=None)
        
        def __str__(self):
                return self.contact_no