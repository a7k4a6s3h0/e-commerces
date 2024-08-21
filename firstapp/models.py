from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length = 100 , unique = True)
    email = models.CharField(max_length=50, null=True,blank=True, unique=True)
    phone = models.CharField(max_length = 13, null=True)
    referal_id = models.CharField(max_length = 50 , null=True , blank=True)
    wallet_amount = models.IntegerField(null=True)
    
    objects = UserManager()

    def __str__(self):
        return self.username



class OTP(models.Model):
    author = models.CharField(max_length=50)
    OTP_digit = models.BigIntegerField(null=False, unique=True)    
    created_time = models.DateTimeField(auto_now_add = True)
    expiry_time = models.DateTimeField(null=False)
    is_verified = models.BooleanField(default=False)
    request_times = models.IntegerField(default=3)