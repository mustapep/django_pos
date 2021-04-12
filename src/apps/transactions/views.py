from django.shortcuts import render, redirect
from django.views import View
from .models import Transactions, DetailTransaction
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
        trn = Transactions.objects.get(id=id)
        dt = DetailTransaction.objects.filter(transaction=trn)
        total = []
        total_item = []
        for d in dt:
            total.append(d.detail_item.price*d.quantity)
            total_item.append(d.quantity)
        return render(request, self.template_name, {
            'dt': dt,
            'total': total,
            'obj': trn,
            't_i': sum(total_item),
            't_p': sum(total)
        })


class PayingView(View):

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        trn.paid_of = True
        trn.update_at = datetime.now()
        trn.save()

        return redirect('/transactions')
