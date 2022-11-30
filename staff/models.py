from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, superuser=False, staff=False):
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_superuser = superuser
        user_obj.is_staff = staff
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.last_login = timezone.now()
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password, first_name, last_name):
        return self.create_user(email, password, first_name, last_name, superuser=True, staff=True)

    def create_staff_user(self, email, password, first_name, last_name):
        return self.create_user(email, password, first_name, last_name, staff=True)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=False, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}:{self.email}'
        
