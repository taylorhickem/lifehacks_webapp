from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Role

@login_required(login_url='hours:login')
def index(request):
    template = loader.get_template('hrs_categories/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


class RoleListView(LoginRequiredMixin, ListView):
    model = Role
    context_object_name = 'roles'
    template_name = 'hrs_categories/role_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['roles'] = context['roles'].filter(
                name__contains=search_input)

        context['search_input'] = search_input
        return context


class RoleDetailView(LoginRequiredMixin, DetailView):
    model = Role
    context_object_name = 'role'
    template_name = 'hrs_categories/role_detail.html'


class RoleCreateView(LoginRequiredMixin, CreateView):
    model = Role
    context_object_name = 'role'
    template_name = 'hrs_categories/role_create.html'
    fields = '__all__'


class RoleUpdateView(LoginRequiredMixin, UpdateView):
    model = Role
    context_object_name = 'role'
    template_name = 'hrs_categories/role_update.html'
    fields = '__all__'


class RoleDeleteView(LoginRequiredMixin, DeleteView):
    model = Role
    context_object_name = 'role'
    template_name = 'hrs_categories/role_delete.html'

