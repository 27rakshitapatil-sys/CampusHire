from django.urls import path
from . import views


urlpatterns = [
    # Student - Notifications
path(
    "notifications/",
    views.notifications,
    name="notifications"
),

    # Student - My Applications
    path(
        "my-applications/",
        views.my_applications,
        name="my_applications"
    ),

    # Student applies for a job
    path(
        "apply/<int:job_id>/",
        views.apply_job,
        name="apply_job"
    ),

    # Recruiter views applicants
    path(
        "applicants/<int:job_id>/",
        views.view_applicants,
        name="view_applicants"
    ),

    # Recruiter shortlists applicant
    path(
        "shortlist/<int:application_id>/",
        views.shortlist_application,
        name="shortlist_application"
    ),

    # Recruiter rejects applicant
    path(
        "reject/<int:application_id>/",
        views.reject_application,
        name="reject_application"
    ),

    # Recruiter selects applicant
    path(
        "select/<int:application_id>/",
        views.select_application,
        name="select_application"
    ),
]