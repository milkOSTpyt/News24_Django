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
    """ Главная страница """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, * , objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    """Вывод новостей по категориям"""
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 4

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], 
        is_published=True).select_related('category')


class DetailNews(DetailView):
    """ Просмотр отдельной новости """
    model = News
    context_object_name = 'news_item'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = News.objects.get(pk=self.kwargs['pk'])
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class CreateNews(LoginRequiredMixin, CreateView):
    """ Создание новости ( Доступно только суперпользователю )"""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новость'
        return context


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
    """ Функция для регистрации пользователя """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
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