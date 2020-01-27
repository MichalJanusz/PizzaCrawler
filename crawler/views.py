from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from forms import *


class MainView(View):
    def get(self, request):
        return render(request, 'crawler/index.html')


class LoginView(View):
    title = 'Logowanie'

    def get(self, request):
        form = LoginForm()
        return render(request, 'crawler/form.html', {'form': form, 'title': self.title})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get("next") if request.GET.get("next") is not None else 'index'
                return redirect(url)
            else:
                return render(request, 'crawler/form.html',
                              {'form': form, 'title': self.title})
        else:
            return render(request, 'crawler/form.html', {'form': form, 'title': self.title})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):
    title = 'Rejestracja'

    def get(self, request):
        form = RegisterForm()
        return render(request, 'crawler/form.html', {'form': form, 'title': self.title})
