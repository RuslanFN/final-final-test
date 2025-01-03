# Generated by Django 4.1.1 on 2024-12-23 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Resipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('about', models.TextField(max_length=1000, verbose_name='Описание')),
                ('duration', models.IntegerField(verbose_name='Длительность')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='resipe_site.category', verbose_name='Категория')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StepResipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('detail', models.TextField(max_length=250, verbose_name='Подробно')),
                ('resipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='resipe_site.resipe')),
            ],
        ),
        migrations.CreateModel(
            name='ImageResipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images%y%m%d')),
                ('resipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='resipe_site.resipe')),
            ],
        ),
    ]
