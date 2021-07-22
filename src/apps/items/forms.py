from django import forms
from .models import Categories


class ItemForm(forms.Form):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label="Category", widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    name = forms.CharField(label='Item Name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    price = forms.CharField(label='Price', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    item_img = forms.ImageField()

class UpdateItemForm(forms.Form):
    id = forms.CharField(required=False, widget=forms.HiddenInput())
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label="Category", widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    name = forms.CharField(label='Item Name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    price = forms.CharField(label='Price', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    item_img = forms.ImageField(required=False)


class AddCategoriesForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

class UnitForm(forms.Form):
    name = forms.CharField(label='Unit', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))



