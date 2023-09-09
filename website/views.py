from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import UpdateView

from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been login successfully')
            return redirect('home')
        else:
            messages.error(request, 'There was an error. Please try again.')
    else:
        return render(request, 'website/home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Your account have been registered successfully!')
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form': form})

    return render(request, 'website/register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "you must have an account")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "your record has been deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You can't delete unless you are logged in..")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record has been added..")
                return redirect('home')
        return render(request, 'website/add_record.html', {'form':form})

    else:
        messages.success(request, 'you must be logged in..')
        return redirect('home')


class UpdateRecord(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Record
    template_name = 'website/update_record.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode']
    success_url = '/'

    def test_func(self):
        return True
