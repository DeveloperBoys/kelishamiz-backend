from rest_framework_nested import routers

from .views import UsersViewSet, ClassifiedsViewSet, UserSearchViewSet


admin_router = routers.SimpleRouter()
admin_router.register(r'users', UsersViewSet)

user_router = routers.NestedSimpleRouter(admin_router, r'users', lookup="user")
user_router.register(
    r'classifieds', ClassifiedsViewSet, basename="user-classifieds")
user_router.register(
    r'searches', UserSearchViewSet, basename="user-searches")
