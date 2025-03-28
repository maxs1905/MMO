from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import AdForm
from .models import Ads, Category, Response, User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class AdsList(ListView):
    model = Ads
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    ordering = '-creared_time'
    paginate_by = 10

class AdsDetail(DetailView):
    model = Ads
    template_name = 'ads_detail.html'
    context_object_name = 'ad'


class AdsCreate(CreateView, LoginRequiredMixin):
    model = Ads
    form_class = AdForm
    template_name = 'create_ad.html'

    login_url = '/login/'

class AdsUpdate(UpdateView, LoginRequiredMixin):
    model = Ads
    form_class = AdForm
    template_name = 'ad_edit.html'
    login_url = '/login/'

    def get_queryset(self):
        return Ads.objects.filter(user=self.request.user)
