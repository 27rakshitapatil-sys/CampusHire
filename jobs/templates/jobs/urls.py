from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.post_job, name="post_job"),
    path("", views.job_list, name="job_list"),
]