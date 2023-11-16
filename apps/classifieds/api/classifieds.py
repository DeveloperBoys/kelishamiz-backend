from typing import List

from django.core.serializers.json import DjangoJSONEncoder

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, route, permissions


from classifieds.schemas import ClassifiedOut, CreateClassified, ReturnCreatedClassified
from classifieds.services import ClassifiedService, ClassifiedImageService, ClassifiedDetailService


@api_controller('/classifieds', tags=['Classifieds'])
class ClassifiedAPI:

    def __init__(self, service=ClassifiedService()):
        self.service = service

    def create_response(self, request, data, status):
        return super().create_response(
            request, data, status, encoder=DjangoJSONEncoder)

    @route.get('')
    def list(self) -> List[ClassifiedOut]:
        return self.service.get_list()

    @route.get('/{classifed_id}')
    def get(
        self,
        classifed_id: int
    ) -> ClassifiedOut:
        return self.service.get(classifed_id)

    @route.post('')
    def create(
        self,
        payload: CreateClassified,
    ) -> ReturnCreatedClassified:
        # owner = self.request.user
        return self.service.create(payload, 1)

    @route.put('')
    def update(
        self,
        payload: CreateClassified
    ) -> ReturnCreatedClassified:
        # owner = self.request.user
        return self.service.update(payload, 1)

    @route.put('')
    def partial_update(
        self,
        payload: CreateClassified
    ) -> ReturnCreatedClassified:
        # owner = self.request.user
        return self.service.partial_update(payload, 1)


@api_controller('/classifieds/<int:pk>/images', tags=['Classified Images'])
class ClassifiedImageAPI:
    ...
