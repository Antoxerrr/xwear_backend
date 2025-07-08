from django.contrib import admin
from .models import Category, Brand, ProductModel, Collab, ProductColor, Product, ProductImage, Price, Size, Chapter


class NameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)


class PriceInline(admin.StackedInline):
    model = Price
    extra = 1
    fields = ('price', 'size')
    autocomplete_fields = ('size',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'category', 'model', 'brand', 'color')
    list_filter = ('category', 'brand', 'model', 'color', 'collab')
    autocomplete_fields = ('category', 'brand', 'model', 'color', 'collab')
    search_fields = ('name', 'article')
    inlines = [ProductImageInline, PriceInline]


@admin.register(Category)
class CategoryAdmin(NameAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(NameAdmin):
    pass


@admin.register(ProductModel)
class ProductModelAdmin(NameAdmin):
    pass


@admin.register(Collab)
class CollabAdmin(NameAdmin):
    pass


@admin.register(Size)
class SizeAdmin(NameAdmin):
    pass


@admin.register(Chapter)
class ChapterAdmin(NameAdmin):
    pass


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)
