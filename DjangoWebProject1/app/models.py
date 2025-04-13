from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Опубликована")
    image = models.FileField(default='cat1.png', verbose_name='Путь к картинке')
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self):
        return self.title
    
    class Meta: 
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")
    
    def __str__(self):
        return f'Комментарий {self.author} к {self.post}'
    
    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering = ["-date"]

# Регистрация моделей в админке
admin.site.register(Blog)
admin.site.register(Comment)