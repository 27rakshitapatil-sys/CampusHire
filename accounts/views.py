from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from students.models import Student


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
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Empty fields

        if not username or not email or not password:

            return render(
                request,
                'register.html',
                {
                    'error': 'Please fill all required fields.'
                }
            )

        # Username check

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'register.html',
                {
                    'error': 'Username already exists'
                }
            )

        # Email check

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

        # Password confirmation

        if confirm_password and password != confirm_password:

            return render(
                request,
                'register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        # Create user

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create student profile

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
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('/accounts/login/')