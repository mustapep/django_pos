from django.shortcuts import render, redirect
from .models import Categories, Items
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AddItemForm
from django.http import HttpResponse
from .item_mixin import IsAutenticate


class ListItemView(LoginRequiredMixin, IsAutenticate, PermissionRequiredMixin, View):
    permission_required = [('items.view_items')]
    template_name = 'sales/list_item.html'
    login_url = '/login'

    def get(self, request):
        obj = Items.objects.all()
        print(request.user.is_authenticated)
        return render(request, self.template_name, {
            'obj': obj
        })


class AddItemView(LoginRequiredMixin, IsAutenticate, PermissionRequiredMixin, View):

    template_name = 'sales/add_item.html'
    login_url = '/login'
    permission_required = [('items.add_items')]

    def get(self, request):
        form = AddItemForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = AddItemForm(request.POST, request.FILES)
        print('isi request.POST : ', request.POST)
        print('isi request.FILES :', request.FILES)
        print('isi form :', form)
        if form.is_valid():
            print('Valid Bre...')
            obj = Items()
            obj.categories = form.cleaned_data['category']
            obj.name = form.cleaned_data['name']
            obj.price = int(form.cleaned_data['price'])
            obj.description = form.cleaned_data['description']
            obj.item_img = request.FILES['item_img']
            obj.save()
            return redirect('/items')
        return HttpResponse(request, form.errors)
