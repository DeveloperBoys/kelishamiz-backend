from django.urls import path
from apps.ads import views

urlpatterns = [
    path('dynamic-fields/', views.DynamicFieldListView.as_view(),
         name='dynamic-field-list'),
    path('dynamic-fields/<int:pk>/',
         views.DynamicFieldDetailView.as_view(), name='dynamic-field-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('ad-details/', views.AdDetailListView.as_view(), name='ad-detail-list'),
    path('ad-details/<int:pk>/', views.AdDetailDetailView.as_view(),
         name='ad-detail-detail'),
    path('ad-images/', views.AdImageView.as_view(), name='ad-image-list'),
    path('ad-images/<int:pk>/', views.AdImageDetailView.as_view(),
         name='ad-image-detail'),
    path('ads/', views.AdListView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad-create')
]
