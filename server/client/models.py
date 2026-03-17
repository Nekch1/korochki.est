from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)


class CourseRequest(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('phone', 'Перевод по номеру телефона'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_name} - {self.user.username}"