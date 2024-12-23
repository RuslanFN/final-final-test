from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, AuthForm, AddReсipe, inline_form, inline_form_image
from . import models
from django.utils.text import slugify
from .slug_generate import SlugGenerator
from django import forms
from django.contrib import messages
from django.db import IntegrityError
from random import choices
# Create your views here.
slug_gen = SlugGenerator()
def remove_recipe(request, slug):
    recipe = get_object_or_404(models.Resipe, slug=slug)
    recipe.delete()
    return redirect('/myrecipes')
def get_resipes(request):
    resipes = models.Resipe.objects.all()
    resipes = resipes if len(resipes) <= 5 else choices(resipes, k=5)
    return render(request, 'resipe_site/resipes-list.html', {'title':'Рецепты', 'resipes':resipes})
def get_my_recipes(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    recipes = request.user.recipes.all()
    return render(request, 'resipe_site/my-resipes-list.html', {'title':'Мои рецепты', 'resipes':recipes})
def detail_recipe(request, slug):
    recipe = models.Resipe.objects.filter(slug=slug).first()
    return render(request, 'resipe_site/recipe-deteil.html', {'title':recipe.title, 'recipe':recipe})
def edit_recipe(request, slug):
    recipe = get_object_or_404(models.Resipe, slug=slug)
    if request.method == 'POST':
        try:
            recipe_form = AddReсipe(request.POST, instance=recipe).save(commit=False)
            recipe_form.slug = slug_gen(recipe_form.title, recipe_form.author.id)
            recipe_form.save()
            stepset = inline_form(request.POST, instance=recipe)
        except IntegrityError:
            messages.error(request, 'У вас уже есть рецепт с таким названием.')
            return redirect(request.path)
        if stepset.is_valid():
                for step in stepset:
                    if step.cleaned_data.get('DELETE') or (not step.cleaned_data.get('title') and not step.cleaned_data.get('detail')):
                        if step.instance.id:
                            step.instance.delete()
                    else:
                        step_instance = step.save(commit=False)
                        step_instance.recipe = recipe
                        step_instance.save()
        else:
            messages.error(request, 'Ошибка в заполнении формы шаги. Отметьте пустые поля шагов.')
            return redirect(request.path)
        images = inline_form_image(request.POST, request.FILES, instance=recipe)
        if images.is_valid():
            for image in images:
                print(image.cleaned_data.get('img'))
                if image.cleaned_data.get('DELET') or not image.cleaned_data.get('img'):
                    if image.instance.id:
                        image.instance.delete()
                else:
                    img = image.save(commit=False)
                    img.resipe = recipe
                    img.save() 
        else:
            messages.error(request, 'Ошибка в заполнении формы. Отметьте пустые поля фотографий')
            return redirect(request.path)
        return redirect('/myrecipes')
    else:
        form = AddReсipe(instance=recipe)
        formset_steps = inline_form(instance = recipe)
        return render(request, 'resipe_site/edit-recipe.html', {'title':'Редактировать рецепт', 'form': form, 'formset': formset_steps, 'image_formset':inline_form_image(instance=recipe)})


def add_recipe(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    if request.POST:    
        resipe_form = AddReсipe(request.POST)
        if resipe_form.is_valid():
            resipe = resipe_form.save(commit=False)
            if not request.user.recipes.filter(title=resipe.title, author=request.user).exists():
                resipe.author = request.user
                resipe.slug = slug_gen(resipe.title, resipe.author.id)
                print(resipe.title)
                resipe.save()
            else:
                messages.error(request, 'У Вас уже есть рецепт с таким названием.')
                return redirect(request.path)
        
            stepset = inline_form(request.POST)
            if stepset.is_valid():
                for step_item in stepset:
                    if not step_item.cleaned_data.get('DELET') and ((step_item.cleaned_data.get('title') and step_item  .cleaned_data.get('detail'))):
                        step = step_item.save(commit=False)
                        step.resipe = resipe
                        step.save() 
            else:
                messages.error(request, 'Ошибка в заполнении формы шаги')
                return redirect(request.path)
            images = inline_form_image(request.POST, request.FILES)
            if images.is_valid():
                for image in images:
                    print(image.cleaned_data.get('img'), 'img')
                    if not image.cleaned_data.get('DELET') and image.cleaned_data.get('img'):
                            img = image.save(commit=False)
                            img.resipe = resipe
                            img.save() 
            else:
                messages.error(request, 'Ошибка в заполнении формы фотки')
                return redirect(request.path)
            
        else:
            messages.error(request, 'Ошибка в заполнении формы форма ')
            return redirect(request.path)
        return redirect('/myrecipes')
    else:
        return render(request, 'resipe_site/add-recipe.html', {'title':'Редактировать рецепт', 'form': AddReсipe(), 'formset': inline_form(), 'image_formset':inline_form_image()})
def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/recipes')
        
    else: 
        logout(request)
        return render(request, 'resipe_site/login.html', {'title':'Авторизация', 'form': AuthForm()})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'resipe_site/register_post.html', {'title':'Регистрация', 'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'resipe_site/register.html', {'title':'Регистрация', 'user_form': user_form})