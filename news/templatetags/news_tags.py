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
    """ Вывод категорий, количество новостей в которых, больше нуля"""
    categories = Category.objects.annotate(cnt=Count('news', 
        filter=F('news__is_published'))).filter(cnt__gt=0)
    return {'categories':categories}