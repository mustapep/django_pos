from django.urls import path
from .views import ListTransactionView, DetailTransactionView, AddDetailTransactionView, EditTransactionView, DeleteTransactionsView

app_name = 'transactoins'
urlpatterns = [
    path('', ListTransactionView.as_view()),
    path('add', AddDetailTransactionView.as_view()),
    path('save', AddDetailTransactionView.as_view()),
    path('edit/<int:id>', EditTransactionView.as_view()),
    path('delete/<int:id>', DeleteTransactionsView.as_view()),
    path('detail_transaction/<int:id>', DetailTransactionView.as_view()),
]
