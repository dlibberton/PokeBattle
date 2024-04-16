from django.contrib.auth.models import AbstractBaseUser 
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email