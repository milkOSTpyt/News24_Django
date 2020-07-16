from django.db import models
from django.urls import reverse

class News(models.Model):
    """ Данный класс работает с базой данных. Здесь созданы колонки в базу с 
    названиями """
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk':self.pk})

    def __str__(self):
        """ Этот метод мы вызываем для того, чтобы мы при вызове в консоли всех 
        данных из БД, видели строку title  """
        return self.title
    
    class Meta:
        """ Здесь мы настраиваем отображения некоторых виджетов """
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at'] # это настройка порядка отображения новостей из БД в админке

class Category(models.Model):
    """ Здесь мы создали таблицу связанную с основной """
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id':self.pk})


    def __str__(self):
        """ Этот метод мы вызываем для того, чтобы мы при вызове в консоли всех 
        данных из БД, видели строку title. И не только в консоли  """
        return self.title
    
    class Meta:
        """ Здесь мы настраиваем отображения некоторых виджетов """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
