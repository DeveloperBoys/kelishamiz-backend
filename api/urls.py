from django.urls import path

from apps.classifieds import views as classified_viws
from apps.likes import views as likes_views
from apps.ads import views as ads_views
from apps.users import views as user_views
from apps.site_settings import views as site_settings_views

classified_urlpatterns = [
    # Category URLs
    path('categories/', classified_viws.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', classified_viws.CategoryDetailView.as_view(),
         name='category-detail'),

    # Classified URLs
    path('images/', classified_viws.ImageView.as_view(),
         name='classified-list'),
    path('classifieds/', classified_viws.CombinedClassifiedListView.as_view(),
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

ads_urlpatterns = [
    path('ad-type-attributes/', ads_views.AdTypeAttributeListCreateView.as_view(),
         name='ad-type-attribute-list-create'),
    path('ad-type-attributes/<int:pk>/',
         ads_views.AdTypeAttributeDetailView.as_view(), name='ad-type-attribute-detail'),

    path('ad-types/', ads_views.AdTypeListCreateView.as_view(),
         name='ad-type-list-create'),
    path('ad-types/<int:pk>/', ads_views.AdTypeDetailView.as_view(),
         name='ad-type-detail'),
    # List and create ClassifiedAd instances
    path('classifiedads/', ads_views.ClassifiedAdListCreateView.as_view(),
         name='classifiedad-list-create'),

    # Retrieve, update, or delete an individual ClassifiedAd instance
    path('classifiedads/<int:pk>/', ads_views.ClassifiedAdRetrieveUpdateDestroyView.as_view(),
         name='classifiedad-retrieve-update-destroy'),
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

site_settings_urlpatterns = [
    path('social-media/', site_settings_views.SocialMediaListCreateView.as_view(),
         name='social-media-list-create'),
    path('social-media/<int:pk>/', site_settings_views.SocialMediaDetailView.as_view(),
         name='social-media-detail'),

    path('app-store-link/', site_settings_views.AppStoreLinkListCreateView.as_view(),
         name='app-store-link-list-create'),
    path('app-store-link/<int:pk>/',
         site_settings_views.AppStoreLinkDetailView.as_view(), name='app-store-link-detail'),

    path('company-info/', site_settings_views.CompanyInfoListCreateView.as_view(),
         name='company-info-list-create'),
    path('company-info/<int:pk>/', site_settings_views.CompanyInfoDetailView.as_view(),
         name='company-info-detail'),

    path('banners/', site_settings_views.BannerListCreateView.as_view(),
         name='banner-list-create'),
    path('banners/<int:pk>/',
         site_settings_views.BannerDetailView.as_view(), name='banner-detail'),
]

urlpatterns = (classified_urlpatterns + likes_urlpatterns +
               user_urlpatterns + site_settings_urlpatterns + ads_urlpatterns)
