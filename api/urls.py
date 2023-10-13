from django.urls import path

from apps.classifieds import views as classified_views
from apps.user_searches import views as search_views
from apps.likes import views as likes_views
from apps.users import views as user_views
from apps.site_settings import views as site_settings_views

classified_urlpatterns = [
    # Category URLs
    path('categories/', classified_views.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', classified_views.CategoryDetailView.as_view(),
         name='category-detail'),

    # Classified URLs
    path('classifieds/', classified_views.ClassifiedListView.as_view(),
         name='classified-list'),
    path('classifieds/<int:pk>/', classified_views.ClassifiedDetailView.as_view(),
         name='classified-detail'),
    path('classifieds/<int:pk>/delete/',
         classified_views.DeleteClassifiedView.as_view(), name='delete-classified'),
    path('classifieds/create/', classified_views.CreateClassifiedView.as_view(),
         name='create-classified'),
    path('classifieds/<int:pk>/images/create/',
         classified_views.CreateClassifiedImageView.as_view(), name='create-classified-image'),
    path('classifieds/<int:pk>/details/create/',
         classified_views.CreateClassifiedDetailView.as_view(), name='create-classified-detail'),
    path('classifieds/<int:pk>/edit/',
         classified_views.EditClassifiedView.as_view(), name='edit-classified'),
    path('classifieds/<int:pk>/images/edit/',
         classified_views.EditClassifiedImageView.as_view(), name='edit-classified-image'),
    path('classifieds/<int:pk>/details/edit/',
         classified_views.EditClassifiedDetailView.as_view(), name='edit-classified-detail'),
    #     path('search/', search_views.SearchView.as_view(), name='search'),
]

likes_urlpatterns = [
    path('likes/create/', likes_views.CreateClassifiedLikeView.as_view(),
         name='create-like'),
    path('likes/get/', likes_views.GetClassifiedLikeView.as_view(), name='get-likes'),
    path('likes/delete/<int:pk>/',
         likes_views.DeleteClassifiedLikeView.as_view(), name='delete-like'),
]


user_urlpatterns = [
    path('admin/login/', user_views.AdminLoginView.as_view(), name='admin-login'),
    path('login', user_views.UserLoginView.as_view(), name='user-login'),
    path('login/verify/', user_views.VerifyApiView.as_view(),
         name='phone_number_verify'),
    path('login/refresh/', user_views.CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('user/data/', user_views.UserDataView.as_view(), name='user_data'),
    path('user/change-information/', user_views.ChangeUserInformationView.as_view(),
         name='change_user_information'),
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
               user_urlpatterns + site_settings_urlpatterns)
