from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail

from .models import Application, Notification
from .forms import ApplicationForm

from students.models import Student
from jobs.models import Job


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
                        "You are logged in as a student. "
                        "Recruiter pages are available only to recruiters."
                    )
                },
                status=403,
            )

        return view_function(request, *args, **kwargs)

    return wrapper


# =========================================================
# STUDENT - APPLY FOR JOB
# =========================================================

@login_required
@student_only
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:

        return render(
            request,
            "apply.html",
            {
                "job": job,
                "error": "Please complete your student profile first."
            }
        )

    already_applied = Application.objects.filter(
        student=student,
        job=job
    ).exists()

    if already_applied:

        return render(
            request,
            "apply.html",
            {
                "job": job,
                "already_applied": True,
                "error": "You have already applied for this job."
            }
        )

    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            Application.objects.create(
                student=student,
                job=job,
                resume=form.cleaned_data["resume"],
                cover_letter=form.cleaned_data["cover_letter"],
                status="Pending"
            )

            return render(
                request,
                "success.html",
                {
                    "job": job
                }
            )

        return render(
            request,
            "apply.html",
            {
                "job": job,
                "form": form,
                "error": (
                    "Please fill the form completely "
                    "before submitting."
                )
            }
        )

    form = ApplicationForm()

    return render(
        request,
        "apply.html",
        {
            "job": job,
            "form": form
        }
    )


# =========================================================
# RECRUITER - VIEW ALL APPLICANTS
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
        "student"
    )

    return render(
        request,
        "applicants.html",
        {
            "job": job,
            "applications": applications
        }
    )


# =========================================================
# RECRUITER - SHORTLIST APPLICATION
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
                f"Hello {application.student.full_name},\n\n"
                f"Congratulations! Your application for "
                f"{application.job.title} has been shortlisted.\n\n"
                f"Please check your CampusHire account "
                f"for more details.\n\n"
                f"Regards,\n"
                f"CampusHire Team"
            ),
            from_email=None,
            recipient_list=[application.student.email],
            fail_silently=True,
        )

    except Exception as error:
        print("EMAIL ERROR:", error)

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# =========================================================
# RECRUITER - REJECT APPLICATION
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

    try:
        send_mail(
            subject="CampusHire - Application Update",
            message=(
                f"Hello {application.student.full_name},\n\n"
                f"Thank you for applying for "
                f"{application.job.title}.\n\n"
                f"Unfortunately, your application was not selected "
                f"for the next stage.\n\n"
                f"We wish you the best for your future opportunities.\n\n"
                f"Regards,\n"
                f"CampusHire Team"
            ),
            from_email=None,
            recipient_list=[application.student.email],
            fail_silently=True,
        )

    except Exception as error:
        print("EMAIL ERROR:", error)

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# =========================================================
# RECRUITER - SELECT APPLICATION
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

    try:
        send_mail(
            subject="CampusHire - Congratulations! You Are Selected",
            message=(
                f"Hello {application.student.full_name},\n\n"
                f"Congratulations! You have been selected for "
                f"{application.job.title}.\n\n"
                f"Please check your CampusHire account for "
                f"further details regarding the next steps.\n\n"
                f"Regards,\n"
                f"CampusHire Team"
            ),
            from_email=None,
            recipient_list=[application.student.email],
            fail_silently=True,
        )

    except Exception as error:
        print("EMAIL ERROR:", error)

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# =========================================================
# STUDENT - MY APPLICATIONS
# =========================================================

@login_required
@student_only
def my_applications(request):

    try:
        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        return render(
            request,
            "my_applications.html",
            {
                "applications": [],
                "error": "Please complete your student profile first."
            }
        )

    applications = Application.objects.filter(
        student=student
    ).select_related(
        "job",
        "job__recruiter"
    ).order_by("-id")

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# STUDENT - NOTIFICATIONS
# =========================================================

@login_required
@student_only
def notifications(request):

    try:
        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        return render(
            request,
            "notifications.html",
            {
                "notifications": []
            }
        )

    notification_list = Notification.objects.filter(
        student=student
    ).order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {
            "notifications": notification_list
        }
    )