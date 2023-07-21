from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Pet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(upload_to='pets/', null=True, blank=True, verbose_name='Фотография')

    def __str__(self):
        return self.name


class Post(models.Model):
    content = models.TextField(verbose_name='Содержание')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    post_date = models.DateTimeField(verbose_name='Дата создания')
    start_date = models.DateTimeField(verbose_name='Дата начала передержки')
    end_date = models.DateTimeField(verbose_name='Дата окончания передержки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    opened = models.BooleanField(default=True, verbose_name='Актуально')
    price = models.IntegerField(verbose_name='Цена')
    pets = models.ManyToManyField(Pet, verbose_name='Питомцы')
