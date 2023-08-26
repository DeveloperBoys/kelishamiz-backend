from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Category, DynamicField, Ad, AdDetail, AdImage


class AdDetailInline(admin.StackedInline):
    model = AdDetail
    extra = 1


class AdImageInline(admin.TabularInline):
    model = AdImage
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


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active',)
    list_filter = ('category', 'is_active',)
    search_fields = ('title', 'category__name',)

    inlines = [AdDetailInline, AdImageInline]


@admin.register(AdDetail)
class AdDetailAdmin(admin.ModelAdmin):
    list_display = ('ad', 'currency_type', 'price',)
    list_filter = ('currency_type',)
    search_fields = ('ad__title',)


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'image',)
    search_fields = ('ad__title',)
