from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Student


# =========================================================
# STUDENT ONLY
# =========================================================

def student_only(view_function):

    @wraps(view_function)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "student"):
            return render(
                request,
                "access_denied.html",
                {
                    "message": (
                        "You do not have permission to access "
                        "the student dashboard."
                    )
                },
                status=403,
            )

        return view_function(request, *args, **kwargs)

    return wrapper


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@login_required
@student_only
def student_dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    return render(
        request,
        "student_dashboard.html",
        {"student": student}
    )


# =========================================================
# STUDENT PROFILE
# =========================================================

@login_required
@student_only
def profile_view(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    return render(
        request,
        "student_profile.html",
        {"student": student}
    )


# =========================================================
# EDIT STUDENT PROFILE
# =========================================================

@login_required
@student_only
def edit_profile(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    if request.method == "POST":

        student.full_name = request.POST.get("full_name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.college = request.POST.get("college")
        student.branch = request.POST.get("branch")
        student.cgpa = request.POST.get("cgpa")
        student.graduation_year = request.POST.get("graduation_year")
        student.skills = request.POST.get("skills")

        if request.FILES.get("resume"):
            student.resume = request.FILES["resume"]

        if request.FILES.get("profile_photo"):
            student.profile_photo = request.FILES["profile_photo"]

        student.save()

        return redirect("student_profile")

    return render(
        request,
        "students/edit_profile.html",
        {"student": student}
    )