from django.urls import include, path

from apps.users import views as user_views
from apps.likes import views as likes_views
from apps.admin_api import views as admin_views
from apps.admin_api.urls import admin_router, user_router
from apps.classifieds import views as classified_views
from apps.site_settings import views as site_settings_views
from apps.payments.views import OrderCreateView

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
    path('classifieds/<int:pk>/edit/',
         classified_views.EditClassifiedView.as_view(), name='edit-classified'),
    #     path('classifieds/<int:pk>/images/create/',
    #          classified_views.CreateClassifiedImageView.as_view(), name='create-classified-image'),
    #     path('classifieds/<int:pk>/images/edit/',
    #          classified_views.EditClassifiedImageView.as_view(), name='edit-classified-image'),
    #     path('classifieds/<int:pk>/details/create/',
    #          classified_views.CreateClassifiedDetailView.as_view(), name='create-classified-detail'),
    #     path('classifieds/<int:pk>/details/edit/',
    #          classified_views.EditClassifiedDetailView.as_view(), name='edit-classified-detail'),
]

likes_urlpatterns = [
    path('likes/create/', likes_views.CreateClassifiedLikeView.as_view(),
         name='create-like'),
    path('likes/get/', likes_views.GetClassifiedLikeView.as_view(), name='get-likes'),
    path('likes/delete/<int:pk>/',
         likes_views.DeleteClassifiedLikeView.as_view(), name='delete-like'),
]


user_urlpatterns = [
    path('login', user_views.UserLoginView.as_view(), name='user-login'),
    path('login/verify/', user_views.VerifyApiView.as_view(),
         name='phone_number_verify'),
    path('login/refresh/', user_views.CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('user/data/', user_views.UserDataView.as_view(), name='user-data'),
    path('user/searches/', user_views.UserSearchesView.as_view(),
         name='user-searches'),
    path('user/classifieds/', user_views.UserClassifiedsView.as_view(),
         name='user-classifieds'),
    path('user/change-information/', user_views.ChangeUserInformationView.as_view(),
         name='change_user_information'),
]


admin_urlpatterns = [
    path('admin/', include(admin_router.urls), name="admin-users"),
    path('admin/', include(user_router.urls)),
    path('admin/login/', admin_views.AdminLoginView.as_view(), name='admin-login'),
]

site_settings_urlpatterns = [
    path('appstore/', site_settings_views.AppStoreLinkListCreateView.as_view()),
    path('appstore/<int:pk>/',
         site_settings_views.AppStoreLinkRetrieveUpdateDestroyView.as_view()),

    path('socialmedia/', site_settings_views.SocialMediaProfileListCreateView.as_view()),
    path('socialmedia/<int:pk>/',
         site_settings_views.SocialMediaProfileRetrieveUpdateDestroyView.as_view()),

    path('company/', site_settings_views.CompanyListCreateView.as_view(),
         name='company-list'),
    path('company/<int:pk>/', site_settings_views.CompanyRetrieveUpdateDestroyView.as_view(),
         name='company-detail'),

    path('banners/', site_settings_views.BannerListCreateView.as_view(),
         name='banner-list-create'),
    path('banners/<int:pk>/',
         site_settings_views.BannerDetailView.as_view(), name='banner-detail'),

    path('locations/', site_settings_views.LocationListView.as_view(),
         name='locations-list-create'),
    path('locations/<int:pk>', site_settings_views.LocationView.as_view(),
         name='locations-detail'),
]


payments_urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order=model-list'),
]


urlpatterns = (
    classified_urlpatterns +
    likes_urlpatterns +
    user_urlpatterns +
    admin_urlpatterns +
    site_settings_urlpatterns +
    payments_urlpatterns
)
