from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, AuthForm, AddResipe, inline_form
from . import models
# Create your views here.

def get_resipes(request):
    resipes = models.Resipe.objects.all()

    return render(request, 'resipe_site/resipes-list.html', {'title':'Рецепты', 'resipes':resipes})
def add_recipe(request):
    print(models.Category.objects.all())
    return render(request, 'resipe_site/add-recipe.html', {'title':'Добавить рецепт', 'form': AddResipe(), 'formset': inline_form()})
def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/categories')
        
    else: 
        logout(request)
        return render(request, 'resipe_site/login.html', {'title':'Авторизация', 'form': AuthForm()})
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