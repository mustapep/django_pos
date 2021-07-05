from django import forms
from .models import Transactions
from apps.items.models import Items
from apps.accounts.models import Members, Sales
from apps.items.models import Categories, Items
from apps.transactions.models import PaymentMethods


class SalesCreateOrderForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Items.objects.order_by('name'),widget=
    forms.Select(attrs={
        'class': 'form-control',
        'placeholder': '- - items - -'
    }))
    quantity = forms.IntegerField(label='Quantity',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder': 'quantity'
        }
    ))

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'search',
            'placeholder': 'search'
        }
    ))


class TransactionForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Members.objects.all(),label='Member', widget=forms.Select(
        attrs={
            'class': 'form-control'
        },
    ), required=False)
    sales = forms.ModelChoiceField(queryset=Sales.objects.all(),label='Sales', widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    payment_method = forms.ModelChoiceField(queryset=PaymentMethods.objects.all(),label='Payment Method', widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    card_number = forms.IntegerField(label='Card Number', widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ), required=False)
    


class PaymentForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))


class CustomerPurchaseForm(forms.Form):
    paying_off = forms.CharField(label='Paying Off',widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'paying off'
        }
    ))



