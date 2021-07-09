from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterMemberForm, CustomersForm, SalesForm
from django.http import HttpResponse
from .models import User, Members, Sales
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from mypermissionmixin.custommixin import ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group


class Login(View):

    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            if Group.objects.get(name='sales') in request.user.groups.all():
                return redirect('/transactions')
            elif Group.objects.get(name='admin') in request.user.groups.all():
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
                return redirect('/transactions')
            elif Group.objects.get(name='admin') in request.user.groups.all():
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
            if request.POST['ptransactionsassword'] == request.POST['password2']:
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
                    return redirect('/transactions')
                elif Group.objects.get(name='admin') in usr.groups.all():
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


"'CRUD Customer View'"


class ListCustomerView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/list_customer.html'
    permission_required = 'accounts.view_members'
    login_url = '/login'

    def get(self, request):

        obj = Members.objects.all()
        return render(request, self.template_name, {
            'obj': obj
        })


class AddCustomerView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/add_customers.html'
    permission_required = 'accounts.add_members'
    login_url = '/login'

    def get(self, request):
        form = CustomersForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = CustomersForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            print('Valid')
            obj = Members()
            obj.customers = form.cleaned_data['customers']
            obj.card_member = form.cleaned_data['card_member']
            obj.gender = form.cleaned_data['gender']
            try:
                obj.photo = request.FILES['photo']
            except:
                pass
            obj.save()
            return redirect('/accounts')
        return HttpResponse(request, form.errors)


class EditCustomerView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/edit_customers.html'
    permission_required = 'accounts.change_members'
    login_url = '/login'

    def get(self, request, id):
        obj = Members.objects.get(id=id)

        data = {
            "customers": obj.customers,
            "gender": obj.gender,
            "card_member": obj.card_member,
            "photo": obj.photo,
        }

        form = CustomersForm(initial=data)

        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        obj = Members.objects.get(id=id)
        form = CustomersForm(request.POST, request.FILES)
        if form.is_valid():
            obj.customers = form.cleaned_data['customers']
            obj.gender = form.cleaned_data['gender']
            obj.card_member = form.cleaned_data['card_member']
            try:
                obj.photo = request.FILES['photo']
            except:
                pass
            obj.save()
            return redirect('/accounts')


class DeleteMemberView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'accounts.delete_members'
    login_url = '/login'

    def get(self, request, id):
        obj = Members.objects.get(id=id)
        obj.delete()
        return redirect('/accounts')



"'End CRUD'"


"'Sales CRUD'"


class ListSalesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/list_sales.html'
    permission_required = 'accounts.view_sales'
    login_url = '/login'

    def get(self, request):
        obj = Sales.objects.all()
        return render(request, self.template_name, {
            'obj': obj
        })


class AddSalesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/add_sales.html'
    permission_required = 'accounts.add_sales'
    login_url = '/login'

    def get(self, request):
        print(request.POST)
        print(request.FILES)
        form = SalesForm()
        return render(request, self.template_name, {
            'form': form
        })


    def post(self, request):
        form = SalesForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                usr = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                grp = Group.objects.get(name='sales')
                usr.first_name = form.cleaned_data['first_name']
                usr.last_name = form.cleaned_data['last_name']
                usr.groups.add(grp)
                usr.save()
                sales = Sales()
                sales.user = usr
                sales.address = form.cleaned_data['address']
                sales.nik_numb = int(form.cleaned_data['nik_numb'])
                sales.ktp_image = request.FILES['ktp_image']
                sales.save()
                return redirect('/accounts/sales')
            messages.error(request, "Password is wrong")
        return HttpResponse(form.errors)


class DeleteSalesView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'accounts.delete_sales'
    login_url = '/login'
    def get(self, request, id):
        s = Sales.objects.get(id=id)
        s.delete()
        return redirect('/accounts/sales')



"'END SALES'"


class AdminLandingPageView(View):
    template_name = 'admin/admin_landingpage.html'

    def get(self, request):
        return render(request, self.template_name)
