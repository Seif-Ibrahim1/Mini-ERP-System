from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SALES = 'SALES', 'Sales'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SALES)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Roles.ADMIN
        
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_sales(self):
        return self.role == self.Roles.SALES