from django.urls import path
from .views import (
    login_view,
    register_view,
    recruiter_register_view,
    logout_view,
)

urlpatterns = [
    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'register/recruiter/',
        recruiter_register_view,
        name='recruiter_register'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),
]