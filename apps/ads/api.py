from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from .models import AdType, AdTypeAttribute, ClassifiedAd, TopClassified
from .schema import AdTypeSchema


class AdTypeAPI(NinjaAPI):
    version = "2.0.0"
    model = AdType

    def list(self, request):
        return self.model.objects.all()

    def retrieve(self, request, pk: int):
        return get_object_or_404(self.model, pk=pk)

    def create(self, request, data: AdTypeSchema):
        return self.model.objects.create(**data)

    def update(self, request, pk: int, data: AdTypeSchema):
        ad_type = get_object_or_404(self.model, pk=pk)
        for attr, value in data.items():
            setattr(ad_type, attr, value)
        ad_type.save()
        return ad_type


class AttributeAPI(NinjaAPI):
    version = "2.0.0"
    model = AdTypeAttribute

    def list(self, request):
        return self.model.objects.all()

    # ... other methods


class ClassifiedAdAPI(NinjaAPI):
    version = "2.0.0"
    model = ClassifiedAd

    def list(self, request):
        return self.model.objects.all()

    # ... other methods


class TopClassifiedAPI(NinjaAPI):
    version = "2.0.0"
    model = TopClassified

    # ... methods


ad_type_api = AdTypeAPI(docs_url=None)
attribute_api = AttributeAPI(docs_url=None)
classified_ad_api = ClassifiedAdAPI(docs_url=None)
top_classified_api = TopClassifiedAPI(docs_url=None)
