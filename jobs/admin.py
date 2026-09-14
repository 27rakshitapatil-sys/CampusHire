from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "recruiter",
        "location",
        "job_type",
        "deadline",
        "created_at",
    )

    ordering = ("-id",)