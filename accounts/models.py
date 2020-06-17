from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_simple_user(self, **kwargs):
        """
        Creates a user object.       
        
        Returns:
            User obj -- the method returns the user object
        """
        user = self.create_user(kwargs.get('email'),
                                password=kwargs.get('password'))
        user.first_name = kwargs.get('first_name')
        user.last_name = kwargs.get('last_name')
        user.phone_number = kwargs.get('phone_number')
        user.status = kwargs.get('status')
        user.sex = kwargs.get("sex")
        user.activity = [kwargs.get('activity', None)]
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), )
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save()
        return user

class User(AbstractBaseUser, BaseModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    USER_ROLES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    email = models.EmailField(unique=True, blank=False)
    objects = UserManager()
    has_logged_in_before = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=200, choices=USER_ROLES, default=ACTIVE)
    phone = models.CharField(max_length=18, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __str__(self):
        return "{}".format(self.email)
