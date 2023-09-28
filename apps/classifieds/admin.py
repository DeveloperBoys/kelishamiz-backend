from django.contrib import admin
from django.forms import inlineformset_factory

from .models import Category, DynamicField, Classified, ClassifiedDetail, ClassifiedImage


class ClassifiedDetailInline(admin.StackedInline):
    model = ClassifiedDetail
    extra = 1


class ClassifiedImageInline(admin.TabularInline):
    model = ClassifiedImage
    min_num = 1
    max_num = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    list_filter = ('parent',)
    search_fields = ('name',)


@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
    search_fields = ('key', 'value',)


@admin.register(Classified)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status',)
    list_filter = ('category', 'status',)
    search_fields = ('title', 'category__name',)

    inlines = [ClassifiedDetailInline, ClassifiedImageInline]


@admin.register(ClassifiedDetail)
class ClassifiedDetailAdmin(admin.ModelAdmin):
    list_display = ('classified', 'currency_type', 'price',)
    list_filter = ('currency_type',)
    search_fields = ('classified__title',)


@admin.register(ClassifiedImage)
class ClassifiedImageAdmin(admin.ModelAdmin):
    list_display = ('classified', 'image',)
    search_fields = ('classified__title',)
