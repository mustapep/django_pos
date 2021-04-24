from django import forms
from apps.accounts import models as mdl_account


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))


class RegisterMemberForm(forms.Form):

    CHOISE_GENDER = (
        ("", "----"),
        ("L", "MALE"),
        ("F", "FEMALE")
    )

    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    member_card = forms.ModelChoiceField(queryset=mdl_account.CardMembers.objects.all(), label="Member Card", widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email'
    }))

    gender = forms.CharField(label="Gender", widget=forms.Select(choices=CHOISE_GENDER, attrs={
        'class': 'form-control'
        }))

    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password'
    }))

    password2 = forms.CharField(label="Confirm Password", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password'
    }))

    photo = forms.ImageField(label='Photo')
