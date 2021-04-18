from django.shortcuts import render
from django.views import View


class Index(View):
    template_name = 'base/base.html'

    def get(self, request):
        return render(request, self.template_name, {
            'tittle': "hello"
        })
