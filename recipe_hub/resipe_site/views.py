from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, AuthForm, AddReсipe, inline_form
from . import models
from django.utils.text import slugify
from .slug_generate import SlugGenerator
# Create your views here.
slug_gen = SlugGenerator()
def get_resipes(request):
    resipes = models.Resipe.objects.all()
    return render(request, 'resipe_site/resipes-list.html', {'title':'Рецепты', 'resipes':resipes})

def edit_reciipe(request, slug):
    recipe = get_object_or_404(models.Resipe, slug=slug)
    if request.method == 'POST':
        recipe_form = AddReсipe(request.POST, instance=recipe).save(commit=False)
        #recipe_form.author = request.user
        recipe_form.slug = slug_gen(recipe_form.title, recipe_form.author.id)
        recipe_form.save()
        if inline_form(request.POST, instance=recipe).is_valid():
            stepset = inline_form(request.POST, instance=recipe)
            for step_item in stepset:
                step = step_item.save(commit=False)
                step.resipe = recipe
                step.save() 
        
        return redirect('/resipes')
    else:
        form = AddReсipe(instance=recipe)
        formset_steps = inline_form(instance = recipe)
        return render(request, 'resipe_site/edit-recipe.html', {'title':'Редактировать рецепт', 'form': form, 'formset': formset_steps})


def add_recipe(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    if request.POST:    
        resipe = AddReсipe(request.POST).save(commit=False)
        resipe.author = request.user
        resipe.slug = slug_gen(resipe.title, resipe.author.id)
        resipe.save()
        if inline_form(request.POST).is_valid():
            stepset = inline_form(request.POST)
            for step_item in stepset:
                step = step_item.save(commit=False)
                step.resipe = resipe
                step.save() 
        return redirect('/resipes')
    else:
        return render(request, 'resipe_site/add-recipe.html', {'title':'Добавить рецепт', 'form': AddReсipe(), 'formset': inline_form()})
def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/resipes')
        
    else: 
        logout(request)
        return render(request, 'resipe_site/login.html', {'title':'Авторизация', 'form': AuthForm()})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        redirect('/login')
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