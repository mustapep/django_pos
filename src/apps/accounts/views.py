from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterMemberForm
from django.http import HttpResponse
from .models import User, Members
from django.contrib import messages


class Login(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm(request.POST)

        return render(request, self.template_name, {
            'form': form
        })


class RegisterView(View):

    template_name = 'register.html'

    def get(self, request):
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
