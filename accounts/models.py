from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TEAM_ROLE_CHOICES = [
        ('Visitor', 'Visitor'),
        ('User', 'User'),
        ('Admin', 'Administrator'),
        ('Super', 'Supervisor'),
    ]
    birthday = models.DateField()
    team_role = models.CharField(max_length=200, choices=TEAM_ROLE_CHOICES, default='Visitor')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.upper()}'
