from django.urls import path

from apps.ads.api import ad_type_api, attribute_api, classified_ad_api, top_classified_api

urlpatterns = [
    path('adtypes/', ad_type_api.urls),
    path('attributes/', attribute_api.urls),
    path('classifiedads/', classified_ad_api.urls),
    path('topclassifieds/', top_classified_api.urls),
]
