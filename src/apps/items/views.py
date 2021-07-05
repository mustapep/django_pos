from django.shortcuts import render, redirect
from .models import Categories, Items
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, ValidatePermissionMixin
from .forms import ItemForm, UpdateItemForm
from django.http import HttpResponse
from mypermissionmixin.custommixin import ValidatePermissionMixin



class ListItemView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'items.view_items'
    template_name = 'sales/list_item.html'
    login_url = '/login'

    def get(self, request):
        obj = Items.objects.all()
        print(request.user.is_authenticated)
        return render(request, self.template_name, {
            'obj': obj,
        })


class AddItemView(LoginRequiredMixin, ValidatePermissionMixin, View):

    template_name = 'sales/add_item.html'
    login_url = '/login'
    permission_required = [('items.add_items')]

    def get(self, request):
        form = ItemForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = ItemForm(request.POST, request.FILES)
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


class UpdateItemView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = [('items.change_items')]
    template_name = 'sales/update_item.html'
    login_url = '/login'

    def get(self, request, id):
        item = Items.objects.get(id=id)
        print(item)
        data = {
            'id': item.id,
            'categories': item.categories,
            'name': item.name,
            'price': item.price,
            'description': item.description,
            'item_img': item.item_img
        }
        form = ItemForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        obj = Items.objects.get(id=id)
        form = UpdateItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj.categories = form.cleaned_data['category']
            print('isi categories', form.cleaned_data['category'])
            obj.name = form.cleaned_data['name']
            obj.price = form.cleaned_data['price']
            obj.description = form.cleaned_data['description']
            try:
                obj.item_img = request.FILES['item_img']
                obj.save()
            except:
                obj.save()
            return redirect('/items')
        return HttpResponse(form.errors)


class DeleteItemView(LoginRequiredMixin, View):
    def get(self, request, id):
        obj = Items.objects.get(id=id)
        obj.delete()
        return redirect('/items')
