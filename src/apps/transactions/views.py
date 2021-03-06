import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .models import Transaction, DetailTransaction, PaymentMethod
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SalesCreateOrderForm, TransactionForm, PaymentForm, CustomerPurchaseForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from apps.accounts.models import Employee
from mypermissionmixin.custommixin import ValidatePermissionMixin
from django.core.exceptions import PermissionDenied
from .helper import income, dateRange
import calendar


class ListTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    template_name = 'list_transaction.html'
    permission_required = 'transactions.view_transaction'

    def get(self, request):
        if request.user.groups.all()[0]=='admin' or request.user.is_superuser:
            t_all = Transaction.objects.filter(paid_of=False)
        else:
            t_all = Transaction.objects.filter(paid_of=False, employee=request.user.employee)
        p = Paginator(t_all, 5)
        page = request.GET.get('page')
        print('p.get_page', p.get_page(page))
        trans = p.get_page(page)
        whoami = request.user.groups.all()[0]

        return render(request, self.template_name, {
            "trans": trans,
            'page': p,
            'data': trans.object_list,
            'whoami': str(whoami)
        })


class ListTransactionsOutView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'list_transactions_out.html'

    def get(self, request):
        t_all = Transaction.objects.filter(paid_of=True)
        p = Paginator(t_all, 5)
        page = request.GET.get('page')
        trans = p.get_page(page)
        whoami = request.user.groups.all()[0]

        return render(request, self.template_name, {
            "trans": trans,
            'page': p,
            'data': trans.object_list,
            'whoami': str(whoami)
        })


class DetailTransactionView(LoginRequiredMixin, ValidatePermissionMixin, View):

    template_name = 'list_detail_trans.html'
    permission_required = 'transactions.view_detailtransaction', 'transactions.delete_detailtransaction'
    login_url = '/login'

    def get(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        fp = CustomerPurchaseForm(request.POST)
        trn = Transaction.objects.get(id=id)
        whoami = request.user.groups.all()[0]
        total = sum([d.item_price*d.quantity for d in trn.detail_transactions.all()])
        total_item = sum([d.quantity for d in trn.detail_transactions.all()])

        return render(request, self.template_name, {
            'dt': trn.detail_transactions.all(),
            'form': form,
            'total': total,
            'obj': trn,
            't_i': total_item,
            't_p': total,
            'id': id,
            'fp': fp,
            'whoami': str(whoami)
        })

    def post(self, request, id):
        form = SalesCreateOrderForm(request.POST)
        if form.is_valid():
            trn = Transaction.objects.get(id=id)
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
        whoami = request.user.groups.all()[0]

        return render(request, self.template_name, {
            'form': form,
            'whoami': str(whoami),
        })

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            trn = Transaction()
            trn.member = form.cleaned_data['member']
            trn.employee = request.user.employee
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

        obj = Transaction.objects.get(id=id)
        whoami = request.user.groups.all()[0]

        data = {
            'member': obj.member,
            'sales': obj.employee,
            'payment_method': obj.payment_method,
            'card_number': obj.card_number,

        }
        form = TransactionForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id,
            'whoami': str(whoami)
        })

    def post(self, request, id):
        form = TransactionForm(request.POST)
        if form.is_valid():
            trn = Transaction.objects.get(id=id)
            trn.member = form.cleaned_data['member']
            trn.employee = request.user
            trn.payment_method = form.cleaned_data['payment_method']
            trn.card_number = form.cleaned_data['card_number']
            trn.save()
            return redirect('/transactions')


class DeleteTransactionsView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = [('transactions.delete_transactions')]

    def get(self, request, id):
        trn = Transaction.objects.get(id=id)
        trn.delete()
        return redirect('/transactions')





"'Payment View'"

class PaymentListView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/payment_list.html'
    permission_required = 'transactions.view_paymentmethods'
    login_url = '/login'

    def get(self, request):
        obj = PaymentMethod.objects.all()
        whoami = request.user.groups.all()[0]
        return render(request, self.template_name, {
            'obj': obj,
            'whoami': str(whoami)
        })


class AddPaymentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/add_payment.html'
    login_url = '/login'
    permission_denied_message = 'items.add_payment'

    def get(self, request):
        form = PaymentForm()
        whoami = request.user.groups.all()[0]
        return render(request, self.template_name, {
            'form': form,
            'whoami': str(whoami)
        })

    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            obj = PaymentMethod()
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/transactions/payment')



class EditPamentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/edit_payment.html'
    permission_required = 'transactions.change_paymentmethods'
    login_url = '/login'

    def get(self, request, id):
        obj = PaymentMethod.objects.get(id=id)
        whoami = request.user.groups.all()[0]
        data = {
            'name': obj.name
        }
        form = PaymentForm(initial=data)
        return render(request, self.template_name, {
            'form': form,
            'id': id,
            'whoami': str(whoami)
        })

    def post(self, request, id):
        form = PaymentForm(request.POST)
        obj = PaymentMethod.objects.get(id=id)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect('/transactions/payment')



class DeletePaymentView(LoginRequiredMixin, ValidatePermissionMixin, View):
    login_url = '/login'
    permission_required = 'transactions.delete_paymentmethods'

    def get(self, request, id):
        obj = PaymentMethod.objects.get(id=id)
        obj.delete()
        return redirect('/transactions/payment')


class CustomerPurchaseView(LoginRequiredMixin, ValidatePermissionMixin, View):
    permission_required = 'transactions.change_transaction'
    login_url = '/login'

    def post(self, request, id):
        form = CustomerPurchaseForm(request.POST)
        whoami = request.user.groups.all()[0]
        if form.is_valid():
            trn = Transaction.objects.get(id=id)
            sub_total=sum([t.item_price*t.quantity for t in trn.detail_transactions.all()])
            if int(form.cleaned_data['paying_off'])>= sub_total:
                if sub_total== 0:
                    messages.warning(request,"please order first")
                    return redirect(f'/transactions/{id}/detail_transaction')
                elif trn.paid_of == False:
                    trn.customer_purchase = int(form.cleaned_data['paying_off'])
                    trn.paid_of = True
                    trn.save()
                else:
                    raise PermissionDenied
            else:
                messages.error(request,"The nominal is wrong")
                return redirect(f'/transactions/{id}/detail_transaction')
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
        whoami = request.user.groups.all()[0]
        self.data, self.month_label = [], []
        today = datetime.datetime.now()
        self.year = today.year
        for x in range(1, 13):
            record = DetailTransaction.objects.filter(transaction__create_at__year=self.year,transaction__create_at__month=x)
            total_income = income(record)
            self.month_label.append(calendar.month_name[x])
            self.data.append(total_income)
        "'Avarage Sales Value'"
        sub_totals = [s.sub_total for s in DetailTransaction.objects.all()]
        avgs = sum(sub_totals) / Transaction.objects.all().count()

        "'Avarage Items per Sales'"
        avis = DetailTransaction.objects.all().count() / Transaction.objects.all().count()
        return render(request, self.template_name, {
            'data': self.data,
            'year': self.year,
            'month_label': self.month_label,
            'trn_wdgt': Transaction.objects.filter(create_at__year=self.year, paid_of=True).count(),
            'avgs': round(avgs, 2),
            'avis': round(avis, 2),
            'whoami': str(whoami)
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
        whoami = request.user.groups.all()[0]
        today = datetime.datetime.now()
        d = calendar.monthrange(today.year,today.month)[1]
        data, date_label = [], []
        for i in range(d+1):
            date_label.append(str(i))
            total_day = []
            trans = Transaction.objects.filter(create_at__year=today.year, create_at__month=today.month, create_at__day=i ,paid_of=True)
            for t in trans:
                sub_totals =[d.sub_total for d in t.detail_transactions.all()]
                total_day.append(sum(sub_totals))
            data.append(sum(total_day))
        "'Avarage Sales Value'"
        print("data: ",data)
        details = DetailTransaction.objects.filter(transaction__create_at__year=today.year, transaction__create_at__month=today.month)
        sub_totals = [s.sub_total for s in details]
        

        "'Avarage Items per Sales'"
        tr = Transaction.objects.filter(create_at__year=today.year, create_at__month=today.month, paid_of=True)
        try:
            avis = details.count()/tr.count()
            avgs = sum(sub_totals) / details.count()
        except:
            avis =0
            avgs = 0
        return render(request, self.template_name, {
            'data': data,
            'month_label': date_label,
            'mn': calendar.month_name[today.month],
            'trn_wdgt': tr.count(),
            'avgs': round(avgs, 2),
            'avis': round(avis, 2),
            'whoami': str(whoami)
        })

class TodayReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/transaction_report_today.html'
    permission_required = ''
    login_url = '/login'
    transactions = None

    def get(self, request):
        whoami = request.user.groups.all()[0]
        "All transactions in today"
        today = datetime.datetime.now()
        y, m, d  = today.year,today.month,today.day
        data , month_label, items= [],[], []
        trans = Transaction.objects.filter(create_at__year=y, create_at__month=m, create_at__day=d, paid_of=True)
        sh, eh=0,1
        for i in range(12):
            month_label.append(f"{sh}-{eh}")
            tsh, teh= trans.filter(create_at__hour=sh), trans.filter(create_at__hour=eh)
            sub_totals = []
            for s in tsh:
                items.append(s.detail_transactions.all().count())
                sub_totals += [d.sub_total for d in s.detail_transactions.all()]
            for e in teh:
                d_eh = e.detail_transactions.all()
                items+=[d.quantity for d in d_eh]
                sub_totals+=[d.sub_total for d in d_eh]
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
            'whoami': str(whoami)
        })
class DateRangeReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = 'admin/report_by_daterange.html'

    def get(self, request):
        whoami = request.user.groups.all()[0]
        data, labels, items = [], [], []
        try:
            tgl = request.GET['date_range']
            start = tgl[0:10]
            end = tgl[13:]
            start = datetime.datetime.strptime(start, '%d/%m/%Y')
            end = datetime.datetime.strptime(end, '%d/%m/%Y')
            for n in dateRange(start, end):
                labels.append(n.strftime("%Y-%m-%d")) #label
                y, m ,d = n.strftime("%Y"), n.strftime("%m"), n.strftime("%d")
                trans = Transaction.objects.filter(create_at__year=y).filter(create_at__month=m).filter(create_at__day=d)
                print(f'Transaksi pada {n.strftime("%Y-%m-%d")} : {trans.count()}')
                trans_total=[]
                for t in trans:
                    dt_total = []
                    dt = DetailTransaction.objects.filter(transaction__id=t.id)
                    for d in dt:
                        items.append(d.quantity)
                        dt_total.append(d.sub_total)
                    trans_total.append(sum(dt_total))
                data.append(sum(trans_total))
            print(f"panjang data : {len(data)}, panjang label {len(labels)}")
            print(data)
            print(labels)
            trn_wgt = Transaction.objects.filter(create_at__date__range=[start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")]).count()
            avgs = sum(data)/trn_wgt
            avis = sum(items)/trn_wgt
        except:
             trn_wgt, avgs, avis, tgl =0, 0 , 0, None
        try:
            pass
        except:
           pass
        return render(request, self.template_name, {
            'data':data,
            'labels':labels,
            'trn_wdgt': trn_wgt,
            "avgs":round(avgs,2),
            'avis':round(avis,2),
            'label': tgl,
            'whoami': str(whoami)

        })
