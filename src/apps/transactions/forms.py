from django import forms
from .models import Transactions
from apps.items.models import Items


class SalesCreateOrderForm(forms.Form):
    quantity = forms.IntegerField()
