from django.db import models
from students.models import Student
from jobs.models import Job


class Application(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    resume = models.FileField(
        upload_to="resumes/",
        null=True,
        blank=True
    )

    cover_letter = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Shortlisted", "Shortlisted"),
            ("Rejected", "Rejected"),
            ("Selected", "Selected"),
        ],
        default="Pending"
    )

    def __str__(self):
        return f"{self.student} - {self.job}"


# =========================================================
# STUDENT - NOTIFICATION
# =========================================================

class Notification(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - {self.message}"