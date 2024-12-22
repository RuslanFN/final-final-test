from django import forms
from django.contrib.auth.models import User
from .models import Category, StepResipe, Resipe, ImageResipe

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтороите пароль', widget=forms.PasswordInput)
    username = forms.CharField(label='Логин', help_text='Латинские буквы, цифры и _')
    first_name = forms.CharField(label='Имя')
    email = forms.CharField(label='Почта', widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    

class StepResipeInline(forms.Form):
    class Meta:
        model = StepResipe
        fields = ['title', 'detail']


class AddReсipe(forms.ModelForm):
    Category = forms.ModelChoiceField(Category.objects.all(), label='Категория')
    class Meta:
        model = Resipe
        fields = ['title', 'about', 'duration', 'Category']
        widgets = {'about':forms.Textarea}


inline_form = forms.inlineformset_factory(Resipe, StepResipe, fields=['title', 'detail'], fk_name='resipe')#, AddResipe, StepResipeInline, fields=['title', 'detail'])
inline_form_image = forms.inlineformset_factory(Resipe, ImageResipe, fields=['img'])
#stepInline = forms.inlineformset_factory(Resipe, StepResipeInline, AddRecipe, StepResipeInline)
class AuthForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())