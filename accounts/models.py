from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('RESPONSABLE', 'Responsable'),
        ('USER', 'Utilisateur'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    service = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
    