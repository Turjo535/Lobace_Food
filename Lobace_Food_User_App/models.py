from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.


class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    otp_code=models.CharField(max_length=6,null=True,blank=True)
    otp_created=models.DateTimeField(blank=True,null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()