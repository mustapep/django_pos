from django.shortcuts import render
from django.views import View
from .forms import LoginForm

class Login(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm(request.POST)

        return render(request, self.template_name, {
            'form': form
        })
