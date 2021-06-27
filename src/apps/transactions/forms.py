from django import forms
from .models import Transactions
from apps.items.models import Items


class SalesCreateOrderForm(forms.Form):
    quantity = forms.IntegerField()

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': ' search',
            'placeholder': 'search'
        }
    ))
