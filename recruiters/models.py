from django.db import models
from django.contrib.auth.models import User


class Recruiter(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recruiter'
    )

    full_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    company_name = models.CharField(max_length=150)

    company_description = models.TextField()

    company_website = models.URLField(
        blank=True,
        null=True
    )

    company_location = models.CharField(max_length=150)

    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.company_name}"