from typing import List

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, route, permissions


from classifieds.services import CategoryService
from classifieds.schemas import CategoryIn, CategoryOut


@api_controller('/categories', tags=['Categories'])
class CategoryAPI:

    def __init__(self, service=CategoryService()):
        self.service = service

    @route.get('')
    def list(self) -> List[CategoryOut]:
        return self.service.get_list()

    @route.get('/{category_id}')
    def get(
        self,
        category_id: int
    ) -> CategoryOut:
        return self.service.get(category_id)

    @route.post('', permissions=permissions.IsAdminUser)
    def create(
        self,
        payload: CategoryIn,
        icon: UploadedFile = File(...)
    ) -> CategoryOut:
        return self.service.create(payload, icon)

    @route.put('/{category_id}', permissions=permissions.IsAdminUser)
    def update(
        self,
        category_id: int,
        payload: CategoryIn,
        icon: UploadedFile = File(...)
    ) -> CategoryOut:
        if icon:
            self.service.update_icon(category_id, icon)
        return self.service.update(category_id, payload)

    @route.patch('/{category_id}', permissions=permissions.IsAdminUser)
    def patch_update(
        self,
        category_id: int,
        payload: CategoryIn | None = None,
        icon: UploadedFile | None = None
    ) -> CategoryOut:
        if icon:
            self.service.update_icon(category_id, icon)
        return self.service.partial_update(category_id, payload)

    @route.delete('/{category_id}', permissions=permissions.IsAdminUser)
    def delete(
        self,
        category_id: int
    ):
        return self.service.delete(category_id)
