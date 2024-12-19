from django.db import models    
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

class Resipe(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, verbose_name='Название')
    about = models.TextField(max_length=1000, verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes', verbose_name='Категория')
    
    def __str__(self):
        return self.title

class ImageResipe(models.Model):
    resipe = models.ForeignKey(Resipe, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=f"images%y%m%d")

    def get_absolute_url(self):
        return self.img.url

    def __str__(self):
        return f'{self.resipe.title}'

class StepResipe(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    detail = models.TextField(max_length=250, verbose_name='Подробно')
    resipe = models.ForeignKey(Resipe, on_delete=models.CASCADE, related_name='steps')
   
    def __str__(self):
        return f'{self.resipe.title} {self.title}'

