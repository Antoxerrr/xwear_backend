from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


class ProductModel(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return f'Модель {self.name}'


class Product(models.Model):

    name = models.CharField('Наименование', max_length=128)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='products')
