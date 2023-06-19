from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission

  
# class UserAccountManager(BaseUserManager):
#   def create_user(self, first_name, last_name, email, password=None):
#     if not email:
#       raise ValueError('Users must have an email address')

#     email = self.normalize_email(email)
#     email = email.lower()

#     user = self.model(
#       first_name=first_name,
#       last_name=last_name,
#       email=email,
#     )

#     user.set_password(password)
#     user.save(using=self._db)

#     return user
  
#   def create_superuser(self, first_name, last_name, email, password=None):
#     user = self.create_user(
#       first_name,
#       last_name,
#       email,
#       password=password,
#     )

#     user.is_staff = True
#     user.is_superuser = True
#     user.save(using=self._db)

#     return user


# class Users(AbstractBaseUser, PermissionsMixin):
#   first_name = models.CharField(max_length=255)
#   last_name = models.CharField(max_length=255)
#   email = models.EmailField(unique=True, max_length=255)
#   is_active = models.BooleanField(default=True)
#   is_staff = models.BooleanField(default=False)
#   groups = models.ManyToManyField(Group, related_name='account_users_set')
#   user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

#   objects = UserAccountManager()

#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = ['first_name', 'last_name']
  
#   class Meta:
#     verbose_name = 'User'
#     verbose_name_plural = 'Users'

#   def __str__(self):
#     return self.email



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
  
  
  
class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

     

   

