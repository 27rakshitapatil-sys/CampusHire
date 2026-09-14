from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Job
from .forms import JobForm

from applications.models import Application
from students.models import Student


# =========================================================
# RECRUITER - POST NEW JOB
# =========================================================

def post_job(request):

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("job_list")

    else:

        form = JobForm()

    return render(
        request,
        "jobs/post_job.html",
        {
            "form": form
        }
    )


# =========================================================
# RECRUITER - EDIT JOB
# =========================================================

@login_required
def edit_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # Only the recruiter who owns the job can edit it
    if not hasattr(request.user, "recruiter"):
        return render(
            request,
            "access_denied.html",
            {
                "message": "You do not have permission to edit this job."
            },
            status=403,
        )

    recruiter = request.user.recruiter

    if job.recruiter != recruiter:
        return render(
            request,
            "access_denied.html",
            {
                "message": "You can only edit jobs posted by your company."
            },
            status=403,
        )

    if request.method == "POST":

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            return redirect("recruiter_dashboard")

    else:

        form = JobForm(
            instance=job
        )

    return render(
        request,
        "jobs/post_job.html",
        {
            "form": form,
            "edit_mode": True,
            "job": job,
        }
    )


# =========================================================
# STUDENT - JOB LIST
# =========================================================

def job_list(request):

    jobs = Job.objects.all().order_by("-id")

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        jobs = jobs.filter(

            Q(title__icontains=search) |

            Q(description__icontains=search) |

            Q(skills__icontains=search) |

            Q(recruiter__full_name__icontains=search) |

            Q(recruiter__company_name__icontains=search)

        )

    # =====================================================
    # LOCATION FILTER
    # =====================================================

    location = request.GET.get(
        "location",
        ""
    ).strip()

    if location:

        jobs = jobs.filter(
            location__icontains=location
        )

    # =====================================================
    # JOB TYPE FILTER
    # =====================================================

    job_type = request.GET.get(
        "job_type",
        ""
    ).strip()

    if job_type:

        jobs = jobs.filter(
            job_type=job_type
        )

    # =====================================================
    # CHECK ALREADY APPLIED JOBS
    # =====================================================

    applied_job_ids = []

    if request.user.is_authenticated:

        try:

            student = Student.objects.get(
                user=request.user
            )

            applied_job_ids = list(

                Application.objects.filter(
                    student=student
                ).values_list(
                    "job_id",
                    flat=True
                )

            )

        except Student.DoesNotExist:

            pass

    # =====================================================
    # JOB TYPE OPTIONS
    # =====================================================

    job_types = Job.JOB_TYPE_CHOICES

    # =====================================================
    # DISPLAY JOBS
    # =====================================================

    return render(

        request,

        "jobs/job_list.html",

        {
            "jobs": jobs,

            "search": search,

            "location": location,

            "job_type": job_type,

            "job_types": job_types,

            "applied_job_ids": applied_job_ids,
        }

    )


# =========================================================
# STUDENT - JOB DETAILS
# =========================================================

def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    return render(

        request,

        "jobs/job_detail.html",

        {
            "job": job
        }

    )