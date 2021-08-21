from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, ValidatePermissionMixin
from .forms import *
from django.http import HttpResponse
from mypermissionmixin.custommixin import ValidatePermissionMixin
from django.core.paginator import Paginator



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
        print(item.categories)
        print(type(item.categories))
        data = {
            'id': item.id,
            'category': item.categories,
            'name': item.name,
            'unit': item.unit,
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
            obj.unit = form.cleaned_data['unit']
            obj.description = form.cleaned_data['description']
            try:
                obj.item_img = request.FILES['item_img']
                obj.save()
            except:
                obj.save()
            return redirect('/items')
        return HttpResponse(form.errors)


class DeleteItemView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'items.deleteitems'
    def get(self, request, id):
        obj = Items.objects.get(id=id)
        obj.delete()
        return redirect('/items')

class ListCategoriesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'list_categories.html'
    login_url = '/login'
    permission_required = 'items.view_categories'

    def get(self, request):
        categories_list = Categories.objects.all()
        p = Paginator(categories_list, 5)
        page = request.GET.get('page')
        categories = p.get_page(page)
        return render(request, self.template_name, {
            'categories': categories,
            'page': p,
            'data': categories.object_list
        })



class AddCategoriesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'add_categories.html'
    login_url = '/login'
    permission_required = 'items.add_categories'

    def get(self, request):
        form = AddCategoriesForm(request.POST)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = AddCategoriesForm(request.POST)
        if form.is_valid():
            obj = Categories()
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/items/categories')
        return HttpResponse(form.errors)

class EditCategoriesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'edit_categories.html'
    login_url = '/login'
    permission_required = 'items.edit_categories'

    def get(self, request, id):
        obj = Categories.objects.get(id=id)
        data = {
            'name': obj.name
        }
        form = AddCategoriesForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        form = AddCategoriesForm(request.POST)
        if form.is_valid():
            obj = Categories.objects.get(id=id)
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/items/categories')
        return HttpResponse(form.errors)


class DeleteCategoriesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'items.delete_categories'
    def get(self, request, id):
        obj = Categories.objects.get(id=id)
        obj.delete()
        return redirect('/items/categories')


class ListUnitView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'list_unit.html'
    login_url = '/login'
    permission_required = 'items.view_unit'

    def get(self, request):
        unit_list = Unit.objects.all()
        p = Paginator(unit_list, 5)
        page = request.GET.get('page')
        unit = p.get_page(page)
        return render(request, self.template_name,{
            'unit': unit,
            'page': p,
            'data': unit.object_list
        })

class AddUnitView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'add_unit.html'
    login_url = '/login'
    permission_required = 'items.add_unit'

    def get(self, request):
        form = UnitForm(request.POST)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = UnitForm(request.POST)
        if form.is_valid():
            obj = Unit()
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/items/unit')
        return HttpResponse(form.errors)


class EditUNitView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'items.edit_unit'
    template_name = 'edit_unit.html'

    def get(self, request, id):
        obj = Unit.objects.get(id=id)
        data = {
            'name': obj.name
        }
        form = UnitForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        form = UnitForm(request.POST)
        if form.is_valid():
            obj = Unit.objects.get(id=id)
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/items/unit')
        return HttpResponse(form.errors)


class DeleteUnitView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'items.delete_unit'
    def get(self, request, id):
        obj = Unit.objects.get(id=id)
        obj.delete()
        return redirect('/items/unit')
