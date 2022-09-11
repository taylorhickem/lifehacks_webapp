from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import HrsAppResource, HrsAppParameter
from .methods import update_events, refresh_resources


def index(request):
    resource_list = HrsAppResource.objects.order_by('-name')
    last_updated = HrsAppParameter.objects.filter(name='last_updated')[0].datetime_value
    template = loader.get_template('hours/index.html')
    context = {
        'resource_list': resource_list,
        'last_updated': last_updated
    }
    return HttpResponse(template.render(context, request))


def refresh(request):
    refresh_resources()
    return HttpResponseRedirect(reverse('hours:index'))


def update(request):
    update_events()
    refresh_resources()
    return HttpResponseRedirect(reverse('hours:index'))
