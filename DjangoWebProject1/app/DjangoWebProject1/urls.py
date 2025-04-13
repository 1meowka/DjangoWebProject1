from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Инициализация административного сайта
admin.autodiscover()

# Функция кастомного входа
def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if username == "admin_di":  # Если это admin_di, перенаправляем в админку
                return redirect("/admin/")
            else:
                return redirect("/")  # Обычный пользователь → на главную
    return render(request, "app/login.html", {
        'form': forms.BootstrapAuthenticationForm(),
        'title': 'Log in',
        'year': datetime.now().year
    })

# Определение маршрутов
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('anketa/', views.anketa, name='anketa'), 
    path('registration/', views.registration, name='registration'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('blog/', views.blog, name ='blog'),
    path('blog/<int:post_id>/', views.blogpost, name='blogpost'),
    path('login/', custom_login, name='login'),  # Кастомный вход
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()