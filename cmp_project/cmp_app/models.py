from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6,
                               validators=[RegexValidator(regex=r'^\d{6}$', message="Pincode must be 6 digits.")],
                               blank=True, null=True)

    # Add custom related_name for 'groups' to avoid conflict with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom reverse relation name
        blank=True
    )

    # Add custom related_name for 'user_permissions' to avoid conflict with auth.User
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Custom reverse relation name
        blank=True
    )

    def __str__(self):
        return self.username


class ContentItem(models.Model):
    author = models.ForeignKey(User, related_name='content', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    categories = models.ManyToManyField('Category')

    def clean(self):
        if len(self.title) > 30:
            raise ValidationError('Title cannot exceed 30 characters')
        if len(self.body) > 300:
            raise ValidationError('Body cannot exceed 300 characters')
        if len(self.summary) > 60:
            raise ValidationError('Summary cannot exceed 60 characters')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
