from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission

  
class UserAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    email = self.normalize_email(email)
    email = email.lower()

    user = self.model(
      first_name=first_name,
      last_name=last_name,
      email=email,
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_superuser(self, first_name, last_name, email, password=None):
    user = self.create_user(
      first_name,
      last_name,
      email,
      password=password,
    )

    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user


class User(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True, max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  groups = models.ManyToManyField(Group, related_name='account_users_set')
  user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']
  
  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'

  def __str__(self):
    return self.email



# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, first_name, last_name, email, password=None):
#       if not email:
#         raise ValueError('Users must have an email address')

#       email = self.normalize_email(email)
#       email = email.lower()

#       user = self.model(
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#       )

#       user.set_password(password)
#       user.save(using=self._db)

#       return user
  
#     def create_superuser(self, first_name, last_name, email, password=None):
#       if not email:
#             raise ValueError("User must have an email")
#       if not password:
#           raise ValueError("User must have a password")
#       if not first_name:
#           raise ValueError("User must have a first name")
        
#       if not last_name:
#           raise ValueError("User must have a last name")
        
#       USERNAME_FIELD = 'email'
#       REQUIRED_FIELDS = ['first_name', 'last_name']
      
#       user = self.create_user(
#         first_name,
#         last_name,
#         email,
#         password=password,
#       )
      
#       user.is_staff = True
#       user.is_superuser = True
#       user.save(using=self._db)

#       return user
  
  
  
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(('email address'), unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

     

   

