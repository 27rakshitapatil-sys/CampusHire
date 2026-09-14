from django.urls import path

from . import views


urlpatterns = [

    path(
        "post/",
        views.post_job,
        name="post_job"
    ),

    path(
        "job/<int:job_id>/",
        views.job_detail,
        name="job_detail"
    ),

    path(
        "",
        views.job_list,
        name="job_list"
    ),

]