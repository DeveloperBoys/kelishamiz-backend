from django.urls import path

from apps.classifieds import views as classified_viws
from apps.likes import views as likes_views

classified_urlpatterns = [
    # DynamicField URLs
    path('dynamic-fields/', classified_viws.DynamicFieldListView.as_view(),
         name='dynamicfield-list'),
    path('dynamic-fields/<int:pk>/',
         classified_viws.DynamicFieldDetailView.as_view(), name='dynamicfield-detail'),

    # Category URLs
    path('categories/', classified_viws.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', classified_viws.CategoryDetailView.as_view(),
         name='category-detail'),

    # ClassifiedDetail URLs
    path('classified-details/', classified_viws.ClassifiedDetailListView.as_view(),
         name='classifieddetail-list'),
    path('classified-details/<int:pk>/',
         classified_viws.ClassifiedDetailDetailView.as_view(), name='classifieddetail-detail'),

    # ClassifiedImage URLs
    path('classified-images/', classified_viws.ClassifiedImageView.as_view(),
         name='classifiedimage-list'),
    path('classified-images/<int:pk>/',
         classified_viws.ClassifiedImageDetailView.as_view(), name='classifiedimage-detail'),

    # Classified URLs
    path('classifieds/', classified_viws.ClassifiedListView.as_view(),
         name='classified-list'),
    path('classifieds/<int:pk>/', classified_viws.ClassifiedDetailView.as_view(),
         name='classified-detail'),
    path('classifieds/create/', classified_viws.ClassifiedCreateView.as_view(),
         name='classified-create'),

]

likes_urlpatterns = [
    path('create-like/', likes_views.CreateClassifiedLikeView.as_view(),
         name='create-like'),
    path('get-likes/', likes_views.GetClassifiedLikeView.as_view(), name='get-likes'),
    path('delete-like/<int:pk>/',
         likes_views.DeleteClassifiedLikeView.as_view(), name='delete-like'),
]

user_urlpatterns = []

urlpatterns = classified_urlpatterns + likes_urlpatterns + user_urlpatterns
