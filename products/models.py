import uuid

from colorfield.fields import ColorField
from django.db import models


class NameModel(models.Model):
    name = models.CharField('Название', max_length=128)

    class Meta:
        abstract = True


class Chapter(NameModel):
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return f'Раздел: {self.name}'


class Category(NameModel):
    chapter = models.ForeignKey(Chapter, verbose_name='Раздел', on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.name}'


class Brand(NameModel):

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return f'Бренд: {self.name}'


class ProductModel(NameModel):

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return f'Модель: {self.name}'


class Collab(NameModel):

    class Meta:
        verbose_name = 'Коллаборация'
        verbose_name_plural = 'Коллаборации'

    def __str__(self):
        return f'Коллаборация: {self.name}'


class ProductColor(NameModel):
    color = ColorField('Цвет', format='hex')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return f'Цвет: {self.name} ({self.color})'


class Product(models.Model):

    name = models.CharField('Наименование', max_length=128, unique=True)
    article = models.CharField('Артикул', max_length=64)

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    model = models.ForeignKey(ProductModel, verbose_name='Модель', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE, null=True, blank=True)

    collab = models.ForeignKey(Collab, verbose_name='Коллаборация', on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(ProductColor, verbose_name='Цвет', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name}'


def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'products/{instance.product.id}/{uuid.uuid4().hex}.{ext}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to=product_image_path)

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

    def __str__(self):
        return f'Изображение продукта <{self.pk}>'


class Size(NameModel):
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return f'Размер: {self.name}'


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    price = models.PositiveIntegerField('Цена')
    size = models.ForeignKey(Size, verbose_name='Размер', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        default_related_name = 'prices'
        constraints = [
            models.UniqueConstraint(fields=['product', 'size'], name='unique_product_size')
        ]

    def __str__(self):
        return f'Цена: {self.pk} ({self.price} руб.)'
