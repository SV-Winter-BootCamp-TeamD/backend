from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, user_email, user_name, user_password=None, **extra_fields):
        if not user_email:
            raise ValueError('Users must have an email address')
        user = self.model(user_email=user_email, user_name=user_name, **extra_fields)
        user.set_password(user_password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email
