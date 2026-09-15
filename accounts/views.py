from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection, transaction

from students.models import Student
from recruiters.models import Recruiter


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        return render(
            request,
            'login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(request, 'login.html')


# =========================================================
# STUDENT REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:

            return render(
                request,
                'register.html',
                {
                    'error': 'Please fill all required fields.'
                }
            )

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Username already exists'
                }
            )

        if User.objects.filter(email=email).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Email already registered'
                }
            )

        if Student.objects.filter(email=email).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Email already registered'
                }
            )

        if Recruiter.objects.filter(email=email).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Email already registered'
                }
            )

        if confirm_password and password != confirm_password:

            return render(
                request,
                'register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Student.objects.create(
            user=user,
            full_name=username,
            email=email,
            phone='',
            college='',
            branch='',
            cgpa=0.00,
            graduation_year=2027,
            skills=''
        )

        return redirect('/accounts/login/')

    return render(request, 'register.html')


# =========================================================
# RECRUITER REGISTER
# =========================================================

def recruiter_register_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        company_description = request.POST.get(
            'company_description',
            ''
        ).strip()
        company_website = request.POST.get(
            'company_website',
            ''
        ).strip()
        company_location = request.POST.get(
            'company_location',
            ''
        ).strip()

        password = request.POST.get('password', '')
        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        # Required fields

        if not username or not full_name or not email or not password:

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Please fill all required fields.'
                }
            )

        # Username check

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Username already exists'
                }
            )

        # Email check

        if User.objects.filter(email=email).exists():

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Email already registered'
                }
            )

        if Student.objects.filter(email=email).exists():

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Email already registered'
                }
            )

        if Recruiter.objects.filter(email=email).exists():

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Email already registered'
                }
            )

        # Password confirmation

        if password != confirm_password:

            return render(
                request,
                'recruiter_register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        # =================================================
        # CREATE USER + RECRUITER SAFELY
        # =================================================

        with transaction.atomic():

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Fix PostgreSQL recruiter ID sequence
            # before creating the recruiter profile.

            if connection.vendor == 'postgresql':

                with connection.cursor() as cursor:

                    cursor.execute("""
                        SELECT MAX(id)
                        FROM recruiters_recruiter
                    """)

                    max_id = cursor.fetchone()[0]

                    if max_id is None:

                        cursor.execute("""
                            SELECT setval(
                                pg_get_serial_sequence(
                                    'recruiters_recruiter',
                                    'id'
                                ),
                                1,
                                false
                            )
                        """)

                    else:

                        cursor.execute("""
                            SELECT setval(
                                pg_get_serial_sequence(
                                    'recruiters_recruiter',
                                    'id'
                                ),
                                %s,
                                true
                            )
                        """, [max_id])

            # Create recruiter profile

            Recruiter.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                company_name=company_name,
                company_description=company_description,
                company_website=company_website or None,
                company_location=company_location
            )

        return redirect('/accounts/login/')

    return render(
        request,
        'recruiter_register.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('/accounts/login/')