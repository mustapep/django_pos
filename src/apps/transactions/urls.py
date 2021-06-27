from django.urls import path
from .views import ListTransactionView, DetailTransactionView, AddDetailTransactionView

app_name = 'transactoins'
urlpatterns = [
    path('', ListTransactionView.as_view()),
    path('detail_transaction/<int:id>', DetailTransactionView.as_view()),
]
