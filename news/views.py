from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import F

class HomeNews(ListView):
    """Здесь мы создаем класс, который отвечает за главную страницу нашего сайта
    model - достает все файлы из нашей таблицы
    template_name - указывает где расположен шаблон для главной страницы
    context_object_name - указывает как называется итерируемый объект (БД)
    paginate_by - указываем количество записей выводиммых на странице"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'title':'Главная'}
    paginate_by = 4

    def get_context_data(self, * , objects_list=None, **kwargs):
        """ Здесь мы определяем контекст для шаблона. Добавляем в словарь title
        и будем работать с ним в шаблоне. """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context
    
    def get_queryset(self):
        """ Даный метод фильтрует вывод новостей на главную страницу. Будут 
        выводиться только те новости, на которыз стоит галочка в поле 
        is_published """
        return News.objects.filter(is_published=True).select_related('category')

""" def index(request):
    news = News.objects.order_by('-created_at')
    context = {
        'news':news,
        'title':'Список новостей',
    }
    return render(request, 'news/index.html', context) """


class NewsByCategory(ListView):
    """Здесь мы написали класс, который отвечает за вывод новостей по категориям
    allow_empty-отвечает за 404 ошибку при вводе несуществующей категории"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 4

    def get_context_data(self, *, objects_list=None, **kwargs):
        """ Здесь мы определяем контекст для шаблона. Добавляем в словарь title
        и будем работать с ним в шаблоне. """
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        """ Даный метод фильтрует вывод новостей в определенной категории 
        select_related - Данный метод объеденяет запросы в базу данных связанные
        с нашими категориями и формирует один запрос, тем самым ускоряя загрузку
        страницы"""
        return News.objects.filter(category_id=self.kwargs['category_id'], 
        is_published=True).select_related('category')
    

""" def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'news':news,
        'category':category,
    }
    return render(request, 'news/category.html', context) """


class View_news(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'

    def get_context_data(self, *, objects_list=None, **kwargs):
        """ Здесь мы определяем контекст для шаблона. Добавляем в словарь title
        и будем работать с ним в шаблоне. """
        context = super().get_context_data(**kwargs)
        context['title'] = News.objects.get(pk=self.kwargs['pk'])
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


""" def view_news(request, news_id):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item':news_item}) """


class CreateNews(LoginRequiredMixin, CreateView):
    """ login_url - После переходиа по ссылке - "Добавить новость" перенаправит 
    в админку на ввод логина и пароля 
    raise_exception - вызывает ошибку 403 после перехода по ссылке на добавление
    новости неавторизированного пользователя
    """
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #login_url = '/admin/' 
    raise_exception = True

    def get_context_data(self, *, objects_list=None, **kwargs):
        """ Здесь мы определяем контекст для шаблона. Добавляем в словарь title
        и будем работать с ним в шаблоне. """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новость'
        return context


""" def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            #news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form':form}) """



def support(request):
    """Данная функция отвечает за тех поддержку и отправку сообщений на почту"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], 
            form.cleaned_data['content'], 'artfilipgalt@gmail.com', 
            ['filiptema40@gmail.com', 'filipovice123@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('support')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка заполнения полей')
    else:
        form = ContactForm()
    return render(request, 'news/support.html', {'form':form})


def register(request):
    """ Функция для регистрации пользователя. После регистрации пользователь 
    автоматически перенаправляется на гланую страницу и уже авторизирован """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировлись')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form':form})


def user_login(request):
    """ Функция для авторизации пользователя """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form':form})


def user_logout(request):
    """ Функция для выхода из аккаунта пользователя """
    logout(request)
    return redirect('home')