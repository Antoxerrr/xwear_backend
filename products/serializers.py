from rest_framework import serializers

from products.models import (
    Product, Category, Brand, ProductModel, Collab, ProductColor, Size, Price, ProductImage, Chapter
)


class NameIdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')


class ProductImageMixin:

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        return [request.build_absolute_uri(img.image.url) for img in images]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta(NameIdSerializer.Meta):
        model = Chapter
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer()

    class Meta:
        model = Category
        fields = ('id', 'name', 'chapter')


class ProductModelSerializer(NameIdSerializer):

    class Meta(NameIdSerializer.Meta):
        model = ProductModel


class BrandSerializer(NameIdSerializer):

    class Meta(NameIdSerializer.Meta):
        model = Brand


class CollabSerializer(NameIdSerializer):

    class Meta(NameIdSerializer.Meta):
        model = Collab


class SizeSerializer(NameIdSerializer):

    class Meta(NameIdSerializer.Meta):
        model = Size


class ProductColorSerializer(NameIdSerializer):

    class Meta(NameIdSerializer.Meta):
        model = ProductColor
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = Price
        fields = '__all__'


class ProductSerializer(ProductImageMixin, serializers.ModelSerializer):

    category = CategorySerializer()
    model = ProductModelSerializer()
    brand = BrandSerializer()
    collab = CollabSerializer()
    color = ProductColorSerializer()
    prices = PriceSerializer(many=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'


class ProductShortSerializer(ProductImageMixin, serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'min_price', 'images')

    def get_min_price(self, obj):
        return obj.min_price


class FiltersDataRequestSerializer(serializers.Serializer):
    selected_chapter = serializers.CharField()


class PriceRangeSerializer(serializers.Serializer):
    min = serializers.IntegerField()
    max = serializers.IntegerField()


class FiltersDataResponseSerializer(serializers.Serializer):
    available_categories = CategorySerializer(many=True)
    available_brands = BrandSerializer(many=True)
    available_models = ProductModelSerializer(many=True)
    available_colors = ProductColorSerializer(many=True)
    available_sizes = SizeSerializer(many=True)
    prices_range = PriceRangeSerializer()
