from django import template
from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    """ Здесь мы написали тэг, который позволяет выводить панель категорий,
        здесь мы прописываем, что выводить только те категории, в которых
        новостей больше нуля и учитывать поле is_published """
    
    #categories = cache.get('categories') # Здесь мы пытаемся получить наши категории из кеша
    #if not categories:
        #'''Если категорий в кеше нет, значит мы туда их заносим на 30 сек'''
        #categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
        #cache.set('categories', categories, 30)

    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {'categories':categories}