from django.shortcuts import render  
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib import auth  
from django.http.response import HttpResponseRedirect  
from django.urls import reverse_lazy  
from django.views.generic import FormView

from users.forms import UserRegistrationForm

def login(request):
    """Форма авторизация реализована с помощью встроенной формы django AuthenticationForm из *django.contrib.auth.forms*"""
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse_lazy('index'))
    else:  
        context = {'form': AuthenticationForm()}  
        return render(request, 'login.html', context)

def logout(request):  
    """Выход из аккаунта реализован с помощью встроенного метода *jango.contrib.auth.logout*"""
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))

def register(request):
    """Форма регистрации реализована с помощью forms.ModelForm"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html', {'user_form': user_form})
