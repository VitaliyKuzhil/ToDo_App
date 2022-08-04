from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, position, password=None):
        """
        Create and save a User with the given position, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            position=position
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, position, password=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            position=position,
            password=password

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    """
    Created a new class called CustomUser that subclasses AbstractUser
    Removed the username field
    Added fields for email, first_name, last_name, position
    Made the email field required and unique
    Set the USERNAME_FIELD -- which defines the unique identifier for the User model -- to email
    Specified that all objects for the class come from the CustomUserManager
    """

    username = None
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    first_name = models.CharField(verbose_name='first_name', max_length=50)
    last_name = models.CharField(verbose_name='last_name', max_length=50)
    position = models.CharField(verbose_name='position', max_length=100)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'position']

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}\n'

    def get_absolute_url(self):
        return reverse('user_profile')
