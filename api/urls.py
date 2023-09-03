from django.urls import path

from apps.classifieds import views as classified_viws
from apps.likes import views as likes_views
from apps.users import views as user_views

classified_urlpatterns = [
    # Category URLs
    path('categories/', classified_viws.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', classified_viws.CategoryDetailView.as_view(),
         name='category-detail'),

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

user_urlpatterns = [
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('login/refresh/', user_views.CustomTokenRefreshView.as_view(),
         name="token_refresh"),
    path('logout/', user_views.LogoutView.as_view(), name="logout"),
    path("signup/", user_views.CreateUserView.as_view(), name='signup'),
    path("verify/", user_views.VerifyApiView.as_view(), name='verify_code'),
    path('new-verify/', user_views.GetNewVerification.as_view(),
         name='new_verify_code'),
    path('change-user-information/', user_views.ChangeUserView.as_view(),
         name='change_user_information')
]

urlpatterns = classified_urlpatterns + likes_urlpatterns + user_urlpatterns
