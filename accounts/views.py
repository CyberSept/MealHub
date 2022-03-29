from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, UpdateUserForm
from polls.models import Food


# Create your views here.


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, user + ' has been registered!')
                return redirect('login')

        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profile_page(request):
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        if request.POST.get('button') == 'name':
            user_form = UpdateUserForm(request.POST, instance=request.user)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile has been updated')
                return redirect('profile')

        elif request.POST.get('button') == 'food':

            if request.POST.get('food'):
                f = Food.objects.get(id=request.POST.get('food'))
                f.hater_user.add(request.user)
                f.save()
        elif request.POST.get('delete'):
            f = Food.objects.get(id=request.POST.get('delete'))
            f.hater_user.remove(request.user)
            f.save()

    food = Food.objects.exclude(hater_user=request.user)
    unwanted = Food.objects.filter(hater_user=request.user)
    context = {'user_form': user_form, 'food': food, 'unwanted': unwanted}
    return render(request, 'accounts/profile.html', context)


class ChangePass(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_message = 'Successfully changed your password'
    success_url = reverse_lazy('profile')
