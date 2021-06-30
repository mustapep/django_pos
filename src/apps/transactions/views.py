from django.shortcuts import render, redirect
from django.views import View
from .models import Transactions, DetailTransaction, PaymentMethods
from apps.items.models import Items
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import SalesCreateOrderForm, SearchForm, TransactionForm, PaymentForm
from datetime import datetime


class ListTransactionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login'
    template_name = 'list_transaction.html'
    permission_required = [('transactions.view_transactions')]

    def get(self, request):

        t_all = Transactions.objects.filter(paid_of=False)

        return render(request, self.template_name, {
            "t_all": t_all
        })


class DetailTransactionView(LoginRequiredMixin, PermissionRequiredMixin, View):

    template_name = 'list_detail_trans.html'
    permission_required = [('transactions.view_detailtransaction')]
    login_url = '/login'

    def get(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        search = SearchForm(request.POST)
        trn = Transactions.objects.get(id=id)
        dt = DetailTransaction.objects.filter(transaction=trn)
        print(dt)
        total = []
        total_item = []
        for d in dt:
            total.append(d.detail_item.price*d.quantity)
            total_item.append(d.quantity)
        return render(request, self.template_name, {
            'dt': dt,
            'form': form,
            'srch': search,
            'total': total,
            'obj': trn,
            't_i': sum(total_item),
            't_p': sum(total),
            'id': id
        })

    def post(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        if form.is_valid():
            trn = Transactions.objects.get(id=id)
            dt = DetailTransaction()
            dt.transaction = trn
            dt.detail_item = form.cleaned_data['item']
            dt.quantity = form.cleaned_data['quantity']
            dt.save()
            return redirect(f'/transactions/{id}/detail_transaction')

class DeleteDetailTransactionsView(View):
    def get(self, request, id, dt_id):
        dt = DetailTransaction.objects.get(id=dt_id)
        dt.delete()
        return redirect(f'/transactions/{id}/detail_transaction')


class PayingView(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        trn.paid_of = True
        trn.update_at = datetime.now()
        trn.save()

        return redirect('/transactions')


class AddDetailTransactionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['transactions.add_transactions']

    template_name = 'sales/add_transactions.html'

    def get(self, request):

        form = TransactionForm(request.POST)

        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['member'])
            print(type(form.cleaned_data['member']))
            trn = Transactions()
            trn.member = form.cleaned_data['member']
            trn.sales = form.cleaned_data['sales']
            trn.payment_method = form.cleaned_data['payment_method']
            trn.card_number = form.cleaned_data['card_number']
            trn.save()
            return redirect('/transactions')

        return redirect('/transactions')


class EditTransactionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'sales/edit_transactions.html'
    permission_required = [('transactions.change_detailtransaction')]

    def get(self, request, id):

        obj = Transactions.objects.get(id=id)
        print(obj.card_number)

        data = {
            'member': obj.member,
            'sales': obj.sales,
            'payment_method': obj.payment_method,
            'card_number': obj.card_number,

        }
        form = TransactionForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        form = TransactionForm(request.POST)
        if form.is_valid():
            trn = Transactions.objects.get(id=id)
            trn.member = form.cleaned_data['member']
            trn.sales = form.cleaned_data['sales']
            trn.payment_method = form.cleaned_data['payment_method']
            trn.card_number = form.cleaned_data['card_number']
            trn.save()
            return redirect('/transactions')


class DeleteTransactionsView(View):

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        trn.delete()
        return redirect('/transactions')





"'Payment View'"

class PaymentListView(View):
    template_name = 'admin/payment_list.html'

    def get(self, request):
        obj = PaymentMethods.objects.all()
        return render(request, self.template_name, {
            'obj': obj
        })


class AddPaymentView(View):
    template_name = 'admin/add_payment.html'

    def get(self, request):
        form = PaymentForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            obj = PaymentMethods()
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/transactions/payment')



class EditPamentView(View):
    template_name = 'admin/edit_payment.html'

    def get(self, request, id):
        obj = PaymentMethods.objects.get(id=id)
        data = {
            'name': obj.name
        }
        form = PaymentForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id
        })

    def post(self, request, id):
        form = PaymentForm(request.POST)
        obj = PaymentMethods.objects.get(id=id)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/transactions/payment')



class DeletePaymentView(View):

    def get(self, request, id):
        obj = PaymentMethods.objects.get(id=id)
        obj.delete()
        return redirect('/transactions/payment')
