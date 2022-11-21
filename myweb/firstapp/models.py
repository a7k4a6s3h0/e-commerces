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

        