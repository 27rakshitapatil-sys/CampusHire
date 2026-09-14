from django.db import models
from recruiters.models import Recruiter


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ]

    recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    requirements = models.TextField()

    skills = models.TextField()

    location = models.CharField(max_length=150)

    salary = models.CharField(max_length=100, blank=True)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
