from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.IntegerField(min_value=0, max_value=999999999, label='УНП')
    last_name = forms.CharField(max_length=150, label="Организация")
    postal_code = forms.CharField(max_length=300, label='Юр. адрес')
    address = forms.CharField(max_length=300, label='Реквизиты')
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'postal_code', 'address',
                  'email']
