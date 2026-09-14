from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from jobs.models import Job
from applications.models import Application, Notification
from .models import Recruiter


# =========================================================
# RECRUITER ONLY
# =========================================================

def recruiter_only(view_function):

    @wraps(view_function)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "recruiter"):
            return render(
                request,
                "access_denied.html",
                {
                    "message": (
                        "You do not have permission to access the "
                        "recruiter dashboard."
                    )
                },
                status=403,
            )

        return view_function(request, *args, **kwargs)

    return wrapper


# =========================================================
# RECRUITER DASHBOARD
# =========================================================

@login_required
@recruiter_only
def dashboard(request):

    recruiter = request.user.recruiter

    jobs = Job.objects.filter(
        recruiter=recruiter
    ).order_by("-id")

    applications = Application.objects.filter(
        job__recruiter=recruiter
    ).select_related(
        "student",
        "job"
    )

    total_applicants = applications.count()

    pending_count = applications.filter(
        status="Pending"
    ).count()

    shortlisted_count = applications.filter(
        status="Shortlisted"
    ).count()

    selected_count = applications.filter(
        status="Selected"
    ).count()

    context = {
        "jobs": jobs,
        "applications": applications,
        "total_applicants": total_applicants,
        "pending_count": pending_count,
        "shortlisted_count": shortlisted_count,
        "selected_count": selected_count,
    }

    return render(
        request,
        "recruiters/dashboard.html",
        context
    )


# =========================================================
# VIEW APPLICANTS FOR A PARTICULAR JOB
# =========================================================

@login_required
@recruiter_only
def view_applicants(request, job_id):

    recruiter = request.user.recruiter

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=recruiter
    )

    applications = Application.objects.filter(
        job=job
    ).select_related(
        "student",
        "job"
    ).order_by("-id")

    return render(
        request,
        "applicants.html",
        {
            "applications": applications,
            "job": job,
        }
    )


# =========================================================
# EDIT JOB
# =========================================================

@login_required
@recruiter_only
def edit_job(request, job_id):

    recruiter = request.user.recruiter

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=recruiter
    )

    if request.method == "POST":

        job.title = request.POST.get(
            "title",
            job.title
        ).strip()

        job.location = request.POST.get(
            "location",
            job.location
        ).strip()

        job.salary = request.POST.get(
            "salary",
            job.salary
        ).strip()

        job.job_type = request.POST.get(
            "job_type",
            job.job_type
        )

        job.deadline = request.POST.get(
            "deadline",
            job.deadline
        )

        job.description = request.POST.get(
            "description",
            job.description
        ).strip()

        job.save()

        return redirect("recruiter_dashboard")

    return render(
        request,
        "recruiters/edit_job.html",
        {
            "job": job
        }
    )


# =========================================================
# DELETE JOB
# =========================================================

@login_required
@recruiter_only
def delete_job(request, job_id):

    recruiter = request.user.recruiter

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=recruiter
    )

    if request.method == "POST":
        job.delete()

    return redirect("recruiter_dashboard")


# =========================================================
# ALL RECRUITER APPLICANTS
# =========================================================

@login_required
@recruiter_only
def applicants(request):

    recruiter = request.user.recruiter

    applications = Application.objects.filter(
        job__recruiter=recruiter
    ).select_related(
        "student",
        "job"
    ).order_by("-id")

    return render(
        request,
        "applicants.html",
        {
            "applications": applications
        }
    )


# =========================================================
# SHORTLIST APPLICATION
# =========================================================

@login_required
@recruiter_only
def shortlist_application(request, application_id):

    recruiter = request.user.recruiter

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=recruiter
    )

    application.status = "Shortlisted"
    application.save()

    Notification.objects.create(
        student=application.student,
        message=(
            f"Your application for "
            f"{application.job.title} has been shortlisted."
        )
    )

    try:
        send_mail(
            subject="CampusHire - Application Shortlisted",
            message=(
                f"Congratulations!\n\n"
                f"Your application for "
                f"'{application.job.title}' "
                f"has been shortlisted by the recruiter.\n\n"
                f"CampusHire Team"
            ),
            from_email=None,
            recipient_list=[application.student.email],
            fail_silently=True,
        )
    except Exception:
        pass

    return redirect("applicants")


# =========================================================
# REJECT APPLICATION
# =========================================================

@login_required
@recruiter_only
def reject_application(request, application_id):

    recruiter = request.user.recruiter

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=recruiter
    )

    application.status = "Rejected"
    application.save()

    Notification.objects.create(
        student=application.student,
        message=(
            f"Your application for "
            f"{application.job.title} has been rejected."
        )
    )

    return redirect("applicants")


# =========================================================
# SELECT APPLICATION
# =========================================================

@login_required
@recruiter_only
def select_application(request, application_id):

    recruiter = request.user.recruiter

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=recruiter
    )

    application.status = "Selected"
    application.save()

    Notification.objects.create(
        student=application.student,
        message=(
            f"Congratulations! You have been selected "
            f"for {application.job.title}."
        )
    )

    return redirect("applicants")


# =========================================================
# RECRUITER PROFILE
# =========================================================

@login_required
@recruiter_only
def recruiter_profile(request):

    recruiter = request.user.recruiter

    if request.method == "POST":

        recruiter.full_name = request.POST.get(
            "full_name",
            recruiter.full_name
        ).strip()

        recruiter.email = request.POST.get(
            "email",
            recruiter.email
        ).strip()

        recruiter.phone = request.POST.get(
            "phone",
            recruiter.phone
        ).strip()

        recruiter.company_name = request.POST.get(
            "company_name",
            recruiter.company_name
        ).strip()

        recruiter.company_description = request.POST.get(
            "company_description",
            recruiter.company_description
        ).strip()

        recruiter.company_website = request.POST.get(
            "company_website",
            recruiter.company_website
        ).strip()

        recruiter.company_location = request.POST.get(
            "company_location",
            recruiter.company_location
        ).strip()

        if request.FILES.get("company_logo"):
            recruiter.company_logo = request.FILES["company_logo"]

        recruiter.save()

        return render(
            request,
            "recruiters/profile.html",
            {
                "recruiter": recruiter,
                "success": "Profile updated successfully!"
            }
        )

    return render(
        request,
        "recruiters/profile.html",
        {
            "recruiter": recruiter
        }
    )