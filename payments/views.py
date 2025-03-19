from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .forms import StudentRegistrationForm,CustomLoginForm, StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Payment

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = StudentRegistrationForm()
    return render(request, 'payments/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomLoginForm()
    return render(request, 'payments/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    payments = Payment.objects.filter(user=request.user).order_by('-date')
    pending_payments = payments.filter(status='Pending')

    context = {
        'user': request.user,
        'payments': payments,
        'pending_payments': pending_payments
    }
    return render(request, 'payments/dashboard.html', context)


