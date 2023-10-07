from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table="user"

    GENDER = [("m","m"),("f","f"),("o","o")]
    ROLE_TYPE = [("super admin","super admin"),("artist manager","artist manager"),("artist","artist")]
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    gender  = models.CharField(choices =GENDER, null=True,blank=True, max_length=100 )
    first_name  = models.CharField( null=True,blank=True, max_length=255 )
    last_name  = models.CharField( null=True,blank=True, max_length=255 )
    dob = models.DateField(null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20)
    role_type = models.CharField(choices =ROLE_TYPE, null=True,blank=True, max_length=100 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



    