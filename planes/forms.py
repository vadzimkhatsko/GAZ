from django import forms
from .models import (
    Contract,
    SumsBYN,
    SumsRUR,
)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = []


class SumsBYNForm(forms.ModelForm):
    class Meta:
        model = SumsBYN
        exclude = ['contract']


class SumsRURForm(forms.ModelForm):
    class Meta:
        model = SumsRUR
        exclude = ['contract']