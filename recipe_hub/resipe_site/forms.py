from django import forms
from django.contrib.auth.models import User
from .models import Category, StepResipe, Resipe

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

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


class AddResipe(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.all(), label='Категория')
    class Meta:
        model = Resipe
        fields = ['title', 'about', 'duration']
        widgets = {'about':forms.Textarea}


inline_form = forms.inlineformset_factory(Resipe, StepResipe, fields=['title', 'detail'], can_delete=True, extra=3)#, AddResipe, StepResipeInline, fields=['title', 'detail'])

#stepInline = forms.inlineformset_factory(Resipe, StepResipeInline, AddRecipe, StepResipeInline)
class AuthForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())