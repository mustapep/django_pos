import datetime

from django.shortcuts import render, redirect
from django.views import View
from .models import Transactions, DetailTransaction, PaymentMethods
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SalesCreateOrderForm, TransactionForm, PaymentForm, CustomerPurchaseForm
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mypermissionmixin.custommixin import ValidatePermissionMixin
from .helper import income
import calendar


class ListTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    template_name = 'list_transaction.html'
    permission_required = 'transactions.view_transactions'

    def get(self, request):

        t_all = Transactions.objects.filter(paid_of=False)

        return render(request, self.template_name, {
            "t_all": t_all
        })


class ListTransactionsOutView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'list_transactions_out.html'

    def get(self, request):
        t_all = Transactions.objects.filter(paid_of=True)

        return render(request, self.template_name, {
            "t_all": t_all
        })


class DetailTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):

    template_name = 'list_detail_trans.html'
    permission_required = 'transactions.view_detailtransaction', 'transactions.delete_detailtransaction'
    login_url = '/login'

    def get(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        fp = CustomerPurchaseForm(request.POST)
        trn = Transactions.objects.get(id=id)
        dt = DetailTransaction.objects.filter(transaction=trn)
        print(dt)
        total = []
        total_item = []
        for d in dt:
            total.append(d.item_price*d.quantity)
            total_item.append(d.quantity)

        return render(request, self.template_name, {
            'dt': dt,
            'form': form,
            'total': total,
            'obj': trn,
            't_i': sum(total_item),
            't_p': sum(total),
            'id': id,
            'fp': fp
        })

    def post(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        if form.is_valid():
            trn = Transactions.objects.get(id=id)
            dt = DetailTransaction()
            dt.transaction = trn
            dt.detail_item = form.cleaned_data['item']
            dt.item_price = int(dt.detail_item.price)
            dt.quantity = form.cleaned_data['quantity']
            dt.sub_total = dt.item_price*dt.quantity
            dt.save()
            return redirect(f'/transactions/{id}/detail_transaction')


class DeleteDetailTransactionsView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'transactions.delete_detailtransaction'
    login_url = '/login'

    def get(self, request, id, dt_id):
        dt = DetailTransaction.objects.get(id=dt_id)
        dt.delete()
        return redirect(f'/transactions/{id}/detail_transaction')


class AddTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'sales/add_transactions.html'
    permission_required = 'transactions.add_detailtransaction'
    login_url = '/login'

    def get(self, request):

        form = TransactionForm(request.POST)

        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['card_number'])
            print(type(form.cleaned_data['member']))
            trn = Transactions()
            trn.member = form.cleaned_data['member']
            trn.sales = form.cleaned_data['sales']
            trn.payment_method = form.cleaned_data['payment_method']
            try:
                trn.card_number = form.cleaned_data['card_number']
            except:
                pass

            trn.save()
            return redirect('/transactions')

        return redirect('/transactions')


class EditTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'sales/edit_transactions.html'
    permission_required = 'transactions.change_transactions'
    login_url = '/login'

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


class DeleteTransactionsView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = [('transactions.delete_transactions')]

    def get(self, request, id):
        trn = Transactions.objects.get(id=id)
        trn.delete()
        return redirect('/transactions')





"'Payment View'"

class PaymentListView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/payment_list.html'
    permission_required = 'transactions.view_paymentmethods'
    login_url = '/login'

    def get(self, request):
        obj = PaymentMethods.objects.all()
        return render(request, self.template_name, {
            'obj': obj
        })


class AddPaymentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/add_payment.html'
    login_url = '/login'
    permission_denied_message = 'items.add_payment'

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



class EditPamentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/edit_payment.html'
    permission_required = 'transactions.change_paymentmethods'
    login_url = '/login'

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



class DeletePaymentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'transactions.delete_paymentmethods'

    def get(self, request, id):
        obj = PaymentMethods.objects.get(id=id)
        obj.delete()
        return redirect('/transactions/payment')


class CustomerPurchaseView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'transactions.change_paymentmethods'
    login_url = '/login'

    def post(self, request, id):
        form = CustomerPurchaseForm(request.POST)
        if form.is_valid():
            trn = Transactions.objects.get(id=id)
            trn.customer_purchase = int(form.cleaned_data['paying_off'])
            trn.paid_of = True
            trn.save()
            return redirect('/transactions')
        return HttpResponse(request, form.errors)



class TransactionsReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/transactions_report.html'
    permission_required = ''
    login_url = '/login'
    data = []
    min_income = None
    max_income = None
    year = ''
    transactions = None
    month_label = []

    def get(self, request):
        self.data, self.month_label = [], []
        today = datetime.datetime.now()
        sy = today.strftime("%Y")
        self.year = sy
        for x in range(1, 13):
            print(calendar.month_name[x], DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=x))
            record = DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=x)
            total_income = income(record)
            self.month_label.append(calendar.month_name[x])
            self.data.append(total_income)
        print(self.month_label)
        print(self.data)
        "'Avarage Sales Value'"
        sub_totals = []
        for s in DetailTransaction.objects.all():
            sub_totals.append(s.sub_total)
        print("sub_total", sub_totals)
        avgs = sum(sub_totals) / Transactions.objects.all().count()

        "'Avarage Items per Sales'"
        avis = DetailTransaction.objects.all().count()/ Transactions.objects.all().count()
        print('Kesini')
        return render(request, self.template_name, {
            'data': self.data,
            'year': self.year,
            'month_label': self.month_label,
            'trn_wdgt': Transactions.objects.filter(paid_of=True).count(),
            'avgs': round(avgs, 2),
            'avis': round(avis, 2),
        })
class MonthlyReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/transaction_report_month.html'
    permission_required = ''
    login_url = '/login'
    min_income = None
    max_income = None
    year = ''
    transactions = None

    def get(self, request):
        today = datetime.datetime.now()
        y = today.strftime("%Y")
        d = calendar.monthrange(int(y),int(today.strftime("%m")))[1]
        trans = Transactions.objects.filter(create_at__year=y).filter(create_at__month=today.strftime("%m")).filter(paid_of=True)
        print("total transaction :",trans.count())
        data, month_label = [], []
        for i in range(d+1):
            month_label.append(str(i))
            total_day = []
            for t in trans:
                sub_totals =[]
                if t.create_at.strftime("%d") == str(i):
                    dt = DetailTransaction.objects.filter(transaction__id=t.id)
                    for d in dt:
                        sub_totals.append(d.sub_total)
                total_day.append(sum(sub_totals))
            data.append(sum(total_day))
        "'Avarage Sales Value'"
        sub_totals = []
        for s in DetailTransaction.objects.filter(transaction__create_at__year=y):
            sub_totals.append(s.sub_total)
        avgs = sum(sub_totals) / DetailTransaction.objects.filter(transaction__create_at__year=y).count()

        "'Avarage Items per Sales'"
        dt = DetailTransaction.objects.filter(transaction__create_at__year=y)
        tr = Transactions.objects.filter(create_at__year=y)
        avis = dt.count()/tr.count()
        return render(request, self.template_name, {
            'data': data,
            'month_label': month_label,
            'mn': calendar.month_name[int(today.strftime("%m"))],
            'trn_wdgt': tr.count(),
            'avgs': round(avgs, 2),
            'avis': round(avis, 2),
        })

class TodayReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/transaction_report_today.html'
    permission_required = ''
    login_url = '/login'
    transactions = None

    def get(self, request):
        "All transactions in today"
        today = datetime.datetime.now()
        y, m, d  = today.strftime('%Y'),today.strftime('%m'),today.strftime('%d')
        data , month_label, items= [],[], []
        trans = Transactions.objects.filter(create_at__year=y).filter(create_at__month=m).filter(create_at__day=d).filter(paid_of=True)
        sh, eh=0,1
        for i in range(12):
            month_label.append(f"{sh}-{eh}")
            tsh, teh= trans.filter(create_at__hour=sh), trans.filter(create_at__hour=eh)
            sub_totals = []
            for s in tsh:
                d_sh = DetailTransaction.objects.filter(transaction__id=s.id)
                items.append(d_sh.count())
                for d in d_sh:
                    sub_totals.append(d.sub_total)
            for e in teh:
                d_eh = DetailTransaction.objects.filter(transaction__id=e.id)
                items.append(d_eh.count())
                for d in d_eh:
                    sub_totals.append(d.sub_total)
            data.append(sum(sub_totals))
            sh+=2
            eh+=2

        "'Avarage Sales Value'"
        try:
            avgs = sum(data) /trans.count()
        except:
            avgs = 0

        "'Avarage Items per Sales'"
        try:
            avis = sum(items)/trans.count()
        except:
            avis=0
        return render(request, self.template_name, {
            'data': data,
            'now': today.strftime("%Y-%m-%d"),
            'month_label': month_label,
            'trn_wdgt': trans.count(),
            'avgs': round(avgs, 2),
            'avis': round(avis, 2),
        })
class DateRangeReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = ''

    def get(self, request):
        pass
