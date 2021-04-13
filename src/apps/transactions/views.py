from django.shortcuts import render, redirect
from django.views import View
from .models import Transactions, DetailTransaction
from apps.items.models import Items
from .forms import SalesCreateOrderForm
from datetime import datetime


class ListTransactionView(View):

    template_name = 'list_transaction.html'

    def get(self, request):

        t_all = Transactions.objects.filter(paid_of=False)

        return render(request, self.template_name, {
            "t_all": t_all
        })


class DetailTransactionView(View):

    template_name = 'list_detail_trans.html'

    def get(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        itm_all = Items.objects.order_by("categories")
        trn = Transactions.objects.get(id=id)
        dt = DetailTransaction.objects.filter(transaction=trn)
        total = []
        total_item = []
        for d in dt:
            total.append(d.detail_item.price*d.quantity)
            total_item.append(d.quantity)
        return render(request, self.template_name, {
            'dt': dt,
            'form': form,
            'items': itm_all[1],
            'total': total,
            'obj': trn,
            't_i': sum(total_item),
            't_p': sum(total)
        })


class AddDtansactionView(View):

    def post(self, request, id, items_id):
        trn = Transactions.objects.get(id=id)
        itm = Items.objects.get(id=items_id)
        form = SalesCreateOrderForm(request.POST)
        print(form.cleaned_data['quantity'])
        if form.is_valid:
            print("iki Valid Bro")
            new_dt = DetailTransaction()
            new_dt.transaction = trn
            new_dt.detail_item = itm
            new_dt.quantity = form.cleaned_data['quantity']
            new_dt.save()
            return redirect('/detail_transaction/{{id}}')
        print("ora valid")


class PayingView(View):

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        trn.paid_of = True
        trn.update_at = datetime.now()
        trn.save()

        return redirect('/transactions')


class AddDetailTransactionView(View): #pas pencet tombol pesan maka mengambil id_trans, items_id, sama quantity

    pass
