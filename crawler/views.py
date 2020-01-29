from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from forms import *
from crawler.models import *
from scraper import ph_scraper, dominos_scraper


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

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():

            # Wyciągam pola do utworzenia obiektu modelu User

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Tworzę obiekt modelu User i przypisuję go do zmiennej user i od razu loguję usera

            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, email=email)

            # Wyciągam pola które służą do wypełnienia obiektu modelu UserInfo

            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house_nr = form.cleaned_data['house_nr']
            flat_nr = form.cleaned_data['flat_nr']
            phone = form.cleaned_data['phone']

            # Tworzę obiekt modelu UserInfo

            UserInfo.objects.create(user=user, city=city, street=street,
                                    house_nr=house_nr, flat_nr=flat_nr, phone=phone)

            # Loguję usera
            login(request, user)
            return redirect('index')

        else:
            return render(request, 'crawler/form.html', {'form': form, 'title': self.title})


def null_resp(resp):
    if resp is None:
        resp = {'name': 'N/A', 'price': 'N/A'}
    return resp


class JsonPHView(View):
    def get(self, request):
        pizza = int(request.GET.get('pizza'))
        resp = ph_scraper(pizza)
        resp = null_resp(resp)
        return JsonResponse(resp)


class JsonDominosView(View):
    def get(self, request):
        pizza = int(request.GET.get('pizza'))
        resp = dominos_scraper(pizza)
        resp = null_resp(resp)
        return JsonResponse(resp)
