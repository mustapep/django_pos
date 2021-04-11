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
