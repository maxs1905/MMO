from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Ads, Response
from .forms import AdForm
from .models import Newsletter
class AdsList(ListView):
    model = Ads
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    ordering = '-create_time'
    paginate_by = 10

class AdsDetail(DetailView):
    model = Ads
    template_name = 'ads_detail.html'
    context_object_name = 'ad'

class AdsCreate(LoginRequiredMixin, CreateView):
    model = Ads
    form_class = AdForm
    template_name = 'create_ad.html'
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not form.cleaned_data.get('category'):
            form.instance.category = None
        return super().form_valid(form)

class AdsUpdate(LoginRequiredMixin, UpdateView):
    model = Ads
    form_class = AdForm
    template_name = 'ad_edit.html'

    def get_success_url(self):
        return reverse_lazy('ads_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(ad__user=self.request.user)

def create_response(request, pk):
    if request.method == 'POST':
        ad = get_object_or_404(Ads, pk=pk)
        text = request.POST.get('text')
        if text:
            Response.objects.create(
                ad=ad,
                user=request.user,
                text=text
            )
            messages.success(request, 'Отклик успешно отправлен!')
        else:
            messages.error(request, 'Текст отклика не может быть пустым')
        return redirect('ads_detail', pk=ad.pk)

def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, ad__user=request.user)
    response.is_accepted = True
    response.save()
    messages.success(request, 'Отклик принят!')
    return redirect('responses')

class NewsletterCreateView(PermissionRequiredMixin, CreateView):
    model = Newsletter
    fields = ['subject', 'message']
    template_name = 'newsletter_create.html'
    permission_required = 'Forum.can_send_newsletter'
    success_url = reverse_lazy('newsletter_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        if 'send_now' in self.request.POST:
            self.object.send()
        return response

class NewsletterListView(PermissionRequiredMixin, ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'
    permission_required = 'Forum.can_view_newsletter'