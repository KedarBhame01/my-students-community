from django.db import models

# Create your models here.
class Admins(models.Model):
    email = models.EmailField(max_length=100)   
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128,default='user') 
    # phone_no = models.CharField(max_length=15,default='0')
    def __str__(self):
        return self.name