from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Student
from jobs.models import Job
from applications.models import Application


# =========================================================
# STUDENT ONLY
# =========================================================

def student_only(view_function):

    @wraps(view_function)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if hasattr(request.user, "recruiter"):
            return render(
                request,
                "access_denied.html",
                {
                    "message": (
                        "You are logged in as a recruiter. "
                        "Student pages are available only to students."
                    )
                },
                status=403,
            )

        return view_function(request, *args, **kwargs)

    return wrapper


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

    if request.method == "POST":

        student.full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        student.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        student.college = request.POST.get(
            "college",
            ""
        ).strip()

        student.branch = request.POST.get(
            "branch",
            ""
        ).strip()

        student.skills = request.POST.get(
            "skills",
            ""
        ).strip()

        cgpa = request.POST.get(
            "cgpa",
            ""
        ).strip()

        if cgpa:
            try:
                student.cgpa = float(cgpa)
            except ValueError:
                return render(
                    request,
                    "student_profile.html",
                    {
                        "student": student,
                        "error": "Please enter a valid CGPA."
                    }
                )

        graduation_year = request.POST.get(
            "graduation_year",
            ""
        ).strip()

        if graduation_year:
            try:
                student.graduation_year = int(
                    graduation_year
                )
            except ValueError:
                return render(
                    request,
                    "student_profile.html",
                    {
                        "student": student,
                        "error": "Please enter a valid graduation year."
                    }
                )

        if request.FILES.get("resume"):
            student.resume = request.FILES["resume"]

        if request.FILES.get("profile_photo"):
            student.profile_photo = request.FILES["profile_photo"]

        student.save()

        return render(
            request,
            "student_profile.html",
            {
                "student": student,
                "success": "Profile saved successfully!"
            }
        )

    return render(
        request,
        "student_profile.html",
        {
            "student": student
        }
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@login_required
@student_only
def student_dashboard(request):

    try:
        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        return render(
            request,
            "student_dashboard.html",
            {
                "student": None,
                "jobs": Job.objects.all().order_by("-id"),
                "applications": [],
                "notifications": [],
                "total_jobs": Job.objects.count(),
                "total_applications": 0,
                "shortlisted": 0,
                "selected": 0,
                "rejected": 0,
                "pending": 0,
                "profile_missing": True,
            }
        )

    jobs = Job.objects.all().order_by("-id")

    applications = Application.objects.filter(
        student=student
    ).select_related(
        "job"
    ).order_by("-id")

    total_jobs = jobs.count()

    total_applications = applications.count()

    shortlisted = applications.filter(
        status="Shortlisted"
    ).count()

    selected = applications.filter(
        status="Selected"
    ).count()

    rejected = applications.filter(
        status="Rejected"
    ).count()

    pending = applications.filter(
        status="Pending"
    ).count()

    notifications = []

    for application in applications:

        if application.status == "Selected":

            notifications.append({
                "type": "selected",
                "message": (
                    f"🎉 Congratulations! You have been selected "
                    f"for {application.job.title}."
                )
            })

        elif application.status == "Shortlisted":

            notifications.append({
                "type": "shortlisted",
                "message": (
                    f"⭐ You have been shortlisted for "
                    f"{application.job.title}."
                )
            })

        elif application.status == "Rejected":

            notifications.append({
                "type": "rejected",
                "message": (
                    f"❌ Your application for "
                    f"{application.job.title} was not selected."
                )
            })

        elif application.status == "Pending":

            notifications.append({
                "type": "pending",
                "message": (
                    f"⏳ Your application for "
                    f"{application.job.title} is under review."
                )
            })

    return render(
        request,
        "student_dashboard.html",
        {
            "student": student,
            "jobs": jobs,
            "applications": applications,
            "notifications": notifications,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "selected": selected,
            "rejected": rejected,
            "pending": pending,
            "profile_missing": False,
        }
    )