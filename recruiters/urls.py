from django.urls import path
from . import views


urlpatterns = [

    # Recruiter Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="recruiter_dashboard"
    ),

    # Recruiter Profile
    path(
        "profile/",
        views.recruiter_profile,
        name="recruiter_profile"
    ),

    # View applicants for a particular job
    path(
        "applicants/<int:job_id>/",
        views.view_applicants,
        name="view_applicants"
    ),

    # All recruiter applicants
    path(
        "applicants/",
        views.applicants,
        name="applicants"
    ),

    # Edit job
    path(
        "edit-job/<int:job_id>/",
        views.edit_job,
        name="edit_job"
    ),

    # Delete job
    path(
        "delete-job/<int:job_id>/",
        views.delete_job,
        name="delete_job"
    ),

    # Application actions
    path(
        "shortlist/<int:application_id>/",
        views.shortlist_application,
        name="shortlist_application"
    ),

    path(
        "reject/<int:application_id>/",
        views.reject_application,
        name="reject_application"
    ),

    path(
        "select/<int:application_id>/",
        views.select_application,
        name="select_application"
    ),
]