from django import forms
from .models import customers, customeraccounts


class customersForm(forms.ModelForm):
    class Meta:
        model = customers
        fields = '__all__'


class customeraccountsForm(forms.ModelForm):
    class Meta:
        model = customeraccounts
        fields = '__all__'

    def clean_balance(self):
        data = self.cleaned_data["balance"]
        if data < 1000:
            raise forms.ValidationError('Amount must be equal to or higher than 1000')
        return data
    