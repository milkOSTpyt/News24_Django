from django.urls import path 
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('support/', support, name='support'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/',NewsByCategory.as_view(),name='category'),
    path('news/<int:pk>/', DetailNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]