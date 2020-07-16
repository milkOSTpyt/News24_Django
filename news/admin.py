from django.contrib import admin
from django import forms
from .models import News, Category
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    """Это класс для ckeditor. Мы указываем на каком поле он будет установлен"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    """ Этот класс создается для редактирования внешнего вида админки
    list_display - это данные, которые будут показываться в админке
    list_display_links - это поля, которые будут кликабельные
    search_fields - это поля, по которым будет производиться поиск
    list_editable - Изменения статуса опубликованности не заходя в новость
    list_filter - Фильтр в админке
    fields - категории, которые будут показываться при редактировании новости
    readonly_fields - категории, которые нельзя изменить при редактировании,
    они нужный так же для того, чтобы джанго разрешил показывать там некоторые
    нередактируемые поля
    save_on_top -добавляет дополнительные кнопки в редактирование новости в верх
    """
    form = NewsAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'update_at', 
    'is_published', 'get_photo')
    list_display_links = ('id', 'title') 
    search_fields = ('title', 'content') 
    list_editable = ('is_published', )
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 
    'is_published', 'views',  'created_at', 'update_at')
    readonly_fields = ('get_photo', 'views',  'created_at', 'update_at')
    save_on_top = True

    def get_photo(self, obj):
        """ Здесь мы выводим в админку фото """
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="75">')
    
    get_photo.short_description = 'Фото' # Задаем название полю фото

class CategoryAdmin(admin.ModelAdmin):
    """ Здесь мы прописываем настройки в админку для второй таблицы """
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

#Здесь мы регистрируем изменения. Сразу регистрируем класс БД, а потом изменения
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админка'
admin.site.site_header = 'Админка'