from django.urls import path

from .views import profile_view, student_dashboard


urlpatterns = [

    path(
        'profile/',
        profile_view,
        name='student_profile'
    ),

    path(
        'dashboard/',
        student_dashboard,
        name='student_dashboard'
    ),

]