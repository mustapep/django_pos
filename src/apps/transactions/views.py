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
        print('----- Get -----')
        print(request.GET.get('seach_year'))
        print(request.GET.get('seach_month'))
        self.data, self.month_label = [], []
        try:
            sy = request.GET['seach_year']
            obj = Transactions.objects.filter(create_at__year=sy)
        except:
            sy = Transactions.objects.order_by('create_at')[0]
            sy = sy.create_at.strftime("%Y")
            obj = Transactions.objects.all().order_by('create_at')
        print('Tampilkan grafik berdasarkan transaksi pertamakali')
        print('Tampilkan data table berdasarkan transaksi pertamakali')
        self.year = sy
        self.transactions = obj
        page = request.GET.get('page', 1)
        print('isi page :', page)
        paginator = Paginator(obj, 5)
        print('paginator :', paginator)
        try:
            trn = paginator.page(page)
        except PageNotAnInteger:
            trn = paginator.page(1)
        except EmptyPage:
            trn = paginator.page(paginator.num_pages)

        print(f'start_index {trn.start_index()} ; end_index : {trn.end_index()}')
        self.transactions = self.transactions[trn.start_index()-1:trn.end_index() + 1]
        for x in range(1, 13):
            print(calendar.month_name[x], DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=x))
            record = DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=x)
            print(record)
            total_income = income(record)
            self.month_label.append(calendar.month_name[x])
            self.data.append(total_income)
        print(self.month_label)
        print(self.data)

        print('Kesini')
        return render(request, self.template_name, {
            'data': self.data,
            'min_income': self.min_income,
            'max_income': self.max_income,
            'year': self.year,
            'month_label': self.month_label,
            'transactions': self.transactions,
            'users': trn,
            'start_index': trn.start_index(),
            'end_index': trn.end_index(),
        })

    # def post(self, request):
    #     print('tampilkan data grafik berdasarkan tahun')
    #     print('data table berdasarkan tahun saja')
    #     sy = request.POST['seach_year']
    #     self.transactions = Transactions.objects.filter(create_at__year=sy).order_by('create_at')
    #     page = request.POST.get('page', 1)
    #     paginator = Paginator(self.transactions, 5)
    #     try:
    #         trn = paginator.page(page)
    #     except PageNotAnInteger:
    #         trn = paginator.page(1)
    #     except EmptyPage:
    #         trn = paginator.page(paginator.num_pages)
    #     self.year = sy
    #     self.transactions = self.transactions[trn.start_index()-1:trn.end_index()+1]
    #     for x in range(1, 13):
    #         record = DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=x)
    #         total_income = income(record)
    #         self.month_label.append(calendar.month_name[x])
    #         self.data.append(total_income)
    #     print(self.month_label)
    #     print(self.data)
    #     return redirect('/transactions/report/annual')


class MonthlyReportView(TransactionsReportView):
    template_name = 'admin/monthly_report.html'

    def get(self, request):
        self.data, self.month_label = [], []
        try:
            sy, sm = request.GET['seach_year'], request.GET['seach_month']
        except:
            pass
        if (request.GET.get('seach_year') != None and request.GET.get('seach_year') != '') and (request.GET.get('seach_month')!= None and request.GET.get('seach_month') != ''):
            print('Tampilkan grafik rata2 pendapatan perbulan berdasarkan tahun')
            print('Tampilkan data transaksi berdasarkan tahun dan bulan')
            self.transactions = Transactions.objects.filter(create_at__year=sy).filter(create_at__month=sm).order_by('create_at')
            self.year = sm
            for i in range(1, calendar.monthrange(int(sy), int(sm))[1]+1):
                dt = DetailTransaction.objects.filter(transaction__create_at__year=sy).filter(transaction__create_at__month=sm).filter(transaction__create_at__day=str(i))
                self.data.append(income(dt))
                self.month_label.append('tgl '+str(i))
        return render(request, self.template_name, {
            'data': self.data,
            'min_income': self.min_income,
            'max_income': self.max_income,
            'year': self.year,
            'month_label': self.month_label,
            'transactions': self.transactions,
        })



class DateRangeReportView(LoginRequiredMixin, ValidatePermissionMixin, View):
    template_name = ''

    def get(self, request):
        pass
