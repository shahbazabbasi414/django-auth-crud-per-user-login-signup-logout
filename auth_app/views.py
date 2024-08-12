from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .decorators import guest_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee
from .forms import EmployeeForm

@guest_required
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

@guest_required
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = UserCreationForm(initial=initial_data)
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

# @login_required
# def dashboard_view(request):
#     return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard_view(request):
    employee_list = Employee.objects.filter(user=request.user)
    paginator = Paginator(employee_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'page_obj': page_obj})

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk, user=request.user)
    if request.method == 'POST':
        employee.delete()
        return redirect('dashboard')
    return render(request, 'delete_employee.html', {'employee': employee})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')