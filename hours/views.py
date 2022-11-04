from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import HrsAppResource, HrsAppParameter
from .methods import update_events, refresh_resources
from .forms import RegisterUserForm


@login_required(login_url='hours:login')
def register_view(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)

            return redirect('hours:login')

    context = {'form': form}
    return render(request, 'hours/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('hours:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('hours:index')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'hours/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('hours:login')


def index(request):
    resource_list = HrsAppResource.objects.order_by('-name')
    last_updated = HrsAppParameter.objects.filter(name='last_updated')[0].datetime_value
    template = loader.get_template('hours/index.html')
    context = {
        'resource_list': resource_list,
        'last_updated': last_updated
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='hours:login')
def refresh(request):
    refresh_resources()
    return HttpResponseRedirect(reverse('hours:index'))


@login_required(login_url='hours:login')
def update(request):
    update_events()
    refresh_resources()
    return HttpResponseRedirect(reverse('hours:index'))