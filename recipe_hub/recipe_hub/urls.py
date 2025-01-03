"""
URL configuration for recipe_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from resipe_site import views
from django.urls import path
from django.conf.urls.static import static
from . import settings
urlpatterns = [
    path('', views.get_resipes),
    path('admin/', admin.site.urls),
    path('register', views.register, name='register'),
    path('<slug:slug>/remove', views.remove_recipe, name='remove'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('recipes', views.get_resipes, name='resipes'),
    path('myrecipes', views.get_my_recipes, name='myresipes'),
    path('add_recipe', views.add_recipe, name='add_resipe'),
    path('<slug:slug>', views.detail_recipe, name='recipe'),
    path('<slug:slug>/edit', views.edit_recipe, name='edit_recipe'),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
