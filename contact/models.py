from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=320)
    is_email_send = models.BooleanField(default=False)
    message = models.TextField()
    
    def __str__(self):
        return self.email
