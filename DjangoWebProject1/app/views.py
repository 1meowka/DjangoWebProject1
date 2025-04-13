"""
Определение views.
"""

from datetime import datetime
import re
from django.shortcuts import render, redirect  # Добавлен redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm  # Добавлен импорт формы регистрации
from .forms import AnketaForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Рендерит главную страницу."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'message': 'Добро пожаловать в Meowdidas!',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Рендерит страницу контактов."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Свяжитесь с нами!',
            'year': datetime.now().year,
        }
    )

def blog(request):
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year':datetime.now().year,
            }
        )

def blogpost(request, post_id):
    post_l = Blog.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post_id)  # Исправлено parametr на post_id

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=post_id)  # Исправлено parametr на post_id
            comment_f.save()
            return redirect('blogpost', post_id=post_l.id)  # Исправлено parametr на post_id
    else:
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_l': post_l,
            'comments': comments,  # Исправлено название переменной
            'form': form,
            'year': datetime.now().year,
        }
    )

def about(request):
    """Рендерит страницу о нас."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Узнайте больше о Meowdidas!',
            'year': datetime.now().year,
        }
    )

def anketa(request):
    """Рендерит страницу с анкетой."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {
        '1': 'Каждый день',
        '2': 'Несколько раз в день',
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    }

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            data['notice'] = 'Да' if form.cleaned_data['notice'] else 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()

    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data
        }
    )

def registration(request):
    """Рендерит страницу регистрации."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # После отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  # Валидация полей формы
            reg_f = regform.save(commit=False)  # Не сохраняем автоматически данные формы
            reg_f.is_staff = False  # Запрещен вход в административный раздел
            reg_f.is_active = True  # Активный пользователь
            reg_f.is_superuser = False  # Не является суперпользователем
            reg_f.date_joined = datetime.now()  # Дата регистрации
            reg_f.last_login = datetime.now()  # Дата последней авторизации
            reg_f.save()  # Сохраняем изменения после добавления данных
            return redirect('home')  # Переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # Создание объекта формы для ввода данных нового пользователя

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # Передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )
        
def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'message': 'Узнайте больше о Meowdidas!',
            'year': datetime.now().year,
        }
    )