from rest_framework_nested import routers

from .views import (
    UsersViewSet,
    UserSearchViewSet,
    ClassifiedsViewSet,
    UserClassifiedsViewSet,
    LikedClassifiedsViewSet
)


admin_router = routers.SimpleRouter()
admin_router.register(r'users', UsersViewSet)
admin_router.register(r'classifieds', UserClassifiedsViewSet)

user_router = routers.NestedSimpleRouter(admin_router, r'users', lookup="user")
user_router.register(
    r'classifieds', ClassifiedsViewSet, basename="user-classifieds")
user_router.register(
    r'searches', UserSearchViewSet, basename="user-searches")
user_router.register(
    r'liked-classifieds', LikedClassifiedsViewSet, basename="user-liked-classifieds")
