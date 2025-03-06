from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Yacht(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='yachts/', blank=True, null=True)
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='available',
    )

    def __str__(self):
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    yacht = models.ForeignKey('Yacht', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=50, default='-')
    surname = models.CharField(max_length=50, default='-')
    phone_number = models.CharField(max_length=15, default="0000000000")
    skipper = models.BooleanField(default=False)
    life_jackets = models.BooleanField(default=False)
    gps = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True, default='')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s rental of {self.yacht.name}"
