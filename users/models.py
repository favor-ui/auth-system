from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user with email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Remove the username field since we're using email as username
    username = None
    
    # Email is used as username (unique identifier)
    email = models.EmailField(
        _('email address'), 
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    
    # Full Name field (required)
    full_name = models.CharField(_('full name'), max_length=255)
    
    # Use email as the username field for authentication
    USERNAME_FIELD = 'email'
    
    # Required fields for createsuperuser command (excluding email since it's USERNAME_FIELD)
    REQUIRED_FIELDS = ['full_name']
    
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the full name."""
        return self.full_name

    def get_short_name(self):
        """Return the short name (first part of full name or email)."""
        return self.full_name.split()[0] if self.full_name else self.email