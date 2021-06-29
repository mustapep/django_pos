from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', ListCustomerView.as_view()),
    path('add_customer', AddCustomerView.as_view()),
    path('save', AddCustomerView.as_view()),
    path('<int:id>/edit', EditCustomerView.as_view()),
    path('<int:id>/update', EditCustomerView.as_view()),
    path('<int:id>/delete', DeleteMemberView.as_view()),
    path('sales', ListSalesView.as_view()),

]
