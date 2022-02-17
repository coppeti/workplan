from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

LOW_LETTER_REGEX = RegexValidator(r'^[a-z]{4,}$')


class User(AbstractUser):
    TEAM_ROLE_CHOICES = [
        ('Visitor', 'Visitor'),
        ('User', 'User'),
        ('Admin', 'Administrator'),
        ('Super', 'Supervisor'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, validators=[LOW_LETTER_REGEX],
                                help_text="Minimum 4 low letters")
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    team_role = models.CharField(max_length=100, choices=TEAM_ROLE_CHOICES, default='Visitor')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.upper()}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()

        super().save(*args, **kwargs)
