from django.urls import path
from . import views

urlpatterns = [
    path('ads', views.AdsList.as_view(), name='ads_list'),
    path('<int:pk>/', views.AdsDetail.as_view(), name='ads_detail'),
    path('create/', views.AdsCreate.as_view(), name='create_ad'),
    path('<int:pk>/ad_edit/', views.AdsUpdate.as_view(), name='ad_edit')

]