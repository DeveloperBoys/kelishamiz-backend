from ..models import Category


class CategoryService:

    def get_list(self):
        categories = Category.objects.filter(
            parent=None).prefetch_related('children')
        return categories

    def get(self, category_id):
        return Category.objects.get(pk=category_id)

    def create(self, payload, icon):
        parent_id = None if 0 == payload.parent else payload.parent

        return Category.objects.create(
            name=payload.name,
            parent_id=parent_id,
            icon=icon
        )

    # def update(self, category_id, payload):
    #     category = Category.objects.get(pk=category_id)
    #     parent_id = None if 0 == payload.parent else payload.parent
    #     if payload:
    #         category.name = payload.name
    #         category.parent_id = parent_id
    #         category.save()
    #         return category
    #     else:
    #         return "No category found for this ID"

    def update(self, category_id, payload):
        category = Category.objects.get(pk=category_id)
        if payload:
            category.name = payload.name
            category.parent_id = payload.parent_id
            category.save(update_fields=['name', 'parent'])
            return category

    def update_icon(self, category_id, icon):
        category = Category.objects.get(category_id)
        category.icon.save(icon)
        category.save()
        return category

    # def partial_update(self, category_id, payload):
    #     category = Category.objects.get(category_id)
    #     if payload:
    #         if payload.name:
    #             category.name = payload.name
    #         if payload.parent:
    #             category.parent_id = payload.parent
    #         category.save()
    #     return category
    def partial_update(self, category_id, payload):
        category = Category.objects.get(pk=category_id)
        if payload:
            updates = {}
            if payload.get('name'):
                updates['name'] = payload['name']
            if payload.get('parent'):
                updates['parent_id'] = payload['parent_id']

        Category.objects.filter(pk=category_id).update(**updates)
        return Category.objects.get(pk=category_id)

    def delete(self, category_id):
        Category.objects.get(pk=category_id).delete()
