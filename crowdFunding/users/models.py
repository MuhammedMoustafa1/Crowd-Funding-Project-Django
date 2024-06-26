from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator,FileExtensionValidator
from datetime import date
from django.core.exceptions import ValidationError
from django.shortcuts import reverse, get_object_or_404
from django.forms import TimeField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, phone, birth_date, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            birth_date = birth_date,
            # photo = photo
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, phone, birth_date, **extra_fields):
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, first_name, last_name, phone, birth_date, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, phone ,birth_date, **extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        return self._create_user(email, password, first_name, last_name, phone, birth_date, **extra_fields)


AUTH_PROVIDERS = {'facebook': 'facebook', 'email': 'email'}


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254,blank=True)
    first_name = models.CharField(max_length=240,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=50, validators=[RegexValidator(r'^01[0-2,5]{1}[0-9]{8}$')],blank=True)
    address = models.CharField( max_length=250)
    photo = models.ImageField(upload_to='users/images',blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    birth_date = models.DateField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    country = models.CharField(null=True,blank=True, max_length=225)
    facebook = models.URLField(null=True, blank=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "phone","birth_date","photo"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def photo_url(self):
        return f"/media/{self.photo}"

