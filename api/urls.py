from django.urls import path
from apps.classifieds import views

urlpatterns = [
    # DynamicField URLs
    path('dynamic-fields/', views.DynamicFieldListView.as_view(),
         name='dynamicfield-list'),
    path('dynamic-fields/<int:pk>/',
         views.DynamicFieldDetailView.as_view(), name='dynamicfield-detail'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(),
         name='category-detail'),

    # ClassifiedDetail URLs
    path('classified-details/', views.ClassifiedDetailListView.as_view(),
         name='classifieddetail-list'),
    path('classified-details/<int:pk>/',
         views.ClassifiedDetailDetailView.as_view(), name='classifieddetail-detail'),

    # ClassifiedImage URLs
    path('classified-images/', views.ClassifiedImageView.as_view(),
         name='classifiedimage-list'),
    path('classified-images/<int:pk>/',
         views.ClassifiedImageDetailView.as_view(), name='classifiedimage-detail'),

    # Classified URLs
    path('classifieds/', views.ClassifiedListView.as_view(), name='classified-list'),
    path('classifieds/<int:pk>/', views.ClassifiedDetailView.as_view(),
         name='classified-detail'),
    path('classifieds/create/', views.ClassifiedCreateView.as_view(),
         name='classified-create'),
]
