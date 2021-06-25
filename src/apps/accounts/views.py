from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterMemberForm
from django.http import HttpResponse
from .models import User, Members
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group


class Login(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            if Group.objects.get(name='sales') in request.user.groups.all():
                return redirect('/items')
            else:
                return redirect('/customer_landingpage')

        form = LoginForm(request.POST)

        return render(request, self.template_name, {
            'form': form
        })


class RegisterView(View):

    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            if Group.objects.get(name='sales') in request.user.groups.all():
                return redirect('/items')
            else:
                return redirect('/customer_landingpage')
        form = RegisterMemberForm(request.POST)
        return render(request, self.template_name, {
            'form': form
        })


class RegisterSaveView(View):

    def post(self, request):
        form = RegisterMemberForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            print('request POST :', request.POST)
            print('request FILES :', request.FILES)
            if request.POST['password'] == request.POST['password2']:
                usr = User()
                usr.username = form.cleaned_data['username']
                usr.first_name = form.cleaned_data['first_name']
                usr.email = form.cleaned_data['email']
                usr.password = form.cleaned_data['password']
                usr.save()
                mmbr = Members()
                mmbr.customers = usr
                mmbr.gender = form.cleaned_data['gender']
                mmbr.card_member = form.cleaned_data['member_card']
                if request.FILES['photo']:
                    mmbr.photo = request.FILES['photo']
                    mmbr.save()
                mmbr.save()
                return redirect('/login')
            else:
                messages.error(request, 'Password is not valid')
        else:
            return HttpResponse(form.errors)

        return redirect('/register')


class LoginProcess(View):

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usr = authenticate(username=username, password=password)
            if usr.is_authenticated:
                if Group.objects.get(name='sales') in usr.groups.all():
                    login(request, usr)
                    return redirect('/items')
                else:
                    login(request, usr)
                    return redirect('/customer_landingpage')
            else:
                messages.error(request, "Username is not found")
                return redirect('/login')
        else:
            return HttpResponse(form.errors)


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/login')


class CustomerLandingPageView(LoginRequiredMixin, View):
    template_name = 'customers/customer_landingPage.html'
    login_url = '/login'

    def get(self, request):
        return render(request, self.template_name)


class AdminLandingPageView(View):
    template_name = 'admin/admin_landingpage.html'

    def get(self, request):
        return render(request, self.template_name)
