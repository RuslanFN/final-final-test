# Generated by Django 5.1.3 on 2024-12-22 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resipe_site', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='resipe',
            name='Category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='resipe_site.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='resipe',
            name='about',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='resipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resipe',
            name='duration',
            field=models.IntegerField(verbose_name='Длительность'),
        ),
        migrations.AlterField(
            model_name='resipe',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='stepresipe',
            name='detail',
            field=models.TextField(max_length=250, verbose_name='Подробно'),
        ),
        migrations.AlterField(
            model_name='stepresipe',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]
