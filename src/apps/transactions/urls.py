from django.urls import path
from .views import *

app_name = 'transactoins'
urlpatterns = [
    path('', ListTransactionView.as_view()),
    path('add', AddDetailTransactionView.as_view()),
    path('save', AddDetailTransactionView.as_view()),
    path('<int:id>/edit', EditTransactionView.as_view()),
    path('<int:id>/update', EditTransactionView.as_view()),
    path('<int:id>/delete', DeleteTransactionsView.as_view()),
    path('<int:id>/detail_transaction', DetailTransactionView.as_view()),
    path('<int:id>/detail_transaction/<int:dt_id>/delete', DeleteDetailTransactionsView.as_view()),
    path('<int:id>/detail_transaction/save', DetailTransactionView.as_view()),

    path('payment', PaymentListView.as_view()),
    path('payment/add', AddPaymentView.as_view()),
    path('payment/save', AddPaymentView.as_view()),
    path('payment/<int:id>/edit', EditPamentView.as_view()),
    path('payment/<int:id>/update', EditPamentView.as_view()),
    path('payment/<int:id>/delete', DeletePaymentView.as_view()),
]
