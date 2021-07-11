from django import forms
from core.models import Order, ContactRequest


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('origin', 'comments', 'is_handled',
                   'created_at', 'chosen_product',)


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        exclude = ('created_at',)



