from django.urls import path
from .views import (
    AdsList, AdsDetail, AdsCreate, AdsUpdate,
    ResponseListView, create_response, accept_response
)

urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),  # Главная страница
    path('ads/<int:pk>/', AdsDetail.as_view(), name='ads_detail'),
    path('ads/create/', AdsCreate.as_view(), name='create_ad'),
    path('ads/<int:pk>/edit/', AdsUpdate.as_view(), name='ad_edit'),
    path('ads/<int:pk>/response/', create_response, name='create_response'),
    path('responses/', ResponseListView.as_view(), name='responses'),
    path('responses/<int:pk>/accept/', accept_response, name='accept_response'),
]