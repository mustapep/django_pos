from django.shortcuts import render
from django.views import View
from .models import Transactions, DetailTransaction


class ListTransactionView(View):

    template_name = 'list_transaction.html'

    def get(self, request):

        t_all = Transactions.objects.all()

        return render(request, self.template_name, {
            "t_all": t_all
        })


class DetailTransactionView(View):

    template_name = 'list_detail_trans.html'

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        dt = DetailTransaction.objects.filter(transaction=trn).select_related('transaction', 'detail_item')
        total = []
        for d in dt:
            total.append(d.detail_item.price*d.quantity)
        return render(request, self.template_name, {
            'dt': dt,
            'total': total
        })
