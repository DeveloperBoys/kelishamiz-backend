from PIL import Image
from io import BytesIO
from typing import List, Optional

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import SimpleUploadedFile

from ninja.errors import HttpError

from apps.classifieds.models import (
    APPROVED,
    DELETED,
    PENDING,
    Classified,
    DynamicField,
    ClassifiedImage,
    ClassifiedDetail
)


class ClassifiedService:

    def get_list(self):
        classifieds = Classified.objects.filter(
            status=APPROVED).order_by('-created_at')
        if not classifieds.exists():
            raise HttpError(404, "No classifieds found")
        return classifieds

    def get(self, classified_id):
        classified = Classified.objects.get(pk=classified_id)
        if not classified:
            raise HttpError(404, "No classifieds found")
        return classified

    def create(self, payload, owner):
        if payload and owner:
            return Classified.objects.create(
                category_id=payload.category,
                title=payload.category,
                owner_id=owner
            )
        return 404

    def update(self, classified_id, payload):
        classified = Classified.objects.get(pk=classified_id)
        if classified and payload:
            classified.category_id = payload.category
            classified.title = payload.title
            classified.save(update_fields=['category', 'title'])
            return classified
        return 404

    def partial_update(self, classified_id, payload):
        updates = {}
        if payload.get('category'):
            updates['category_id'] = payload['category']
        if payload.get('title'):
            updates['title'] = payload['title']

        Classified.objects.filter(pk=classified_id).update(**updates)
        return Classified.objects.get(pk=classified_id)


class ClassifiedImageService:

    def _optimize_image(self, image):
        if image.size > 4*1024*1024:
            output = BytesIO()
            Image.open(image).convert('RGB').save(
                output, format='JPEG', optimize=True, quality=85)
            output.seek(0)
            return SimpleUploadedFile(image.name, output.read())
        return image

    def create_images(self, classified: Classified, images: List[SimpleUploadedFile]) -> List[ClassifiedImage]:
        cached_classified = cache.get(f'classified-{classified.id}')
        if not cached_classified:
            cached_classified = Classified.objects.prefetch_related(
                'classifiedimage_set').get(id=classified.id)
            cache.set(f'classified-{classified.id}', cached_classified, 3600)

        optimized_images = []
        for image in images:
            optimized_image = self._optimize_image(image)
            optimized_images.append(ClassifiedImage(
                classified=cached_classified,
                image=optimized_image))

        ClassifiedImage.objects.bulk_create(optimized_images)
        return optimized_images

    def get_images(self, classified_id: int) -> List[ClassifiedImage]:
        classified = Classified.objects.prefetch_related(
            'classifiedimage_set').get(id=classified_id)
        return classified.classifiedimage_set.all()

    @staticmethod
    def get_image_for_list(classified):
        images = classified.images.order_by('-id')[:5]
        if images:
            return images
        return None

    def get_image(self, image_id: int) -> Optional[ClassifiedImage]:
        return ClassifiedImage.objects.filter(id=image_id).first()

    def update_image(self, image_id, new_image):
        image = self.get_image(image_id)
        if image:
            optimized_image = self._optimize_image(new_image)
            image.image = optimized_image
            image.save()
            return image
        return None

    def delete_image(self, image_id):
        try:
            image = ClassifiedImage.objects.get(id=image_id)
            image.delete()
        except ClassifiedImage.DoesNotExist:
            pass


class ClassifiedDetailService:

    def create(self, payload, classified_id):
        classified = get_object_or_404(Classified, pk=classified_id)
        if payload and classified.status == PENDING:
            dynamic_fields = payload.pop('dynamicFields')
            classified_detail = ClassifiedDetail.objects.create(
                classified=classified,
                **payload
            )
            for dynamic_field in dynamic_fields:
                DynamicField.objects.create(
                    classified_detail=classified_detail,
                    **dynamic_field
                )
            classified.status = PENDING
            classified.save()

            return classified_detail
        return 404

    def update(self, classified_id, payload):
        classified = get_object_or_404(Classified, pk=classified_id)

        if classified.status != DELETED and payload:
            classified_detail = ClassifiedDetail.objects.filter(
                classified=classified)
            classified_detail.update(**payload)
            return classified_detail

    def partial_update(self, classified_id, payload):
        classified = get_object_or_404(Classified, pk=classified_id)

        if classified.status != DELETED and payload:
            updates = {}

            if payload.get('currency_type'):
                updates['currency_type'] = payload['currency_type']

            if payload.get('price'):
                updates['price'] = payload['price']

            if payload.get('is_negotiable'):
                updates['is_negotiable'] = payload['is_negotiable']

            if payload.get('description'):
                updates['description'] = payload['description']

            classified_detail = ClassifiedDetail.objects.filter(
                classified=classified)
            classified_detail.update(**updates)
            return classified_detail
