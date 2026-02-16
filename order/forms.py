from django import forms
from .models import Order, OrderItem
from django import forms
from django.forms import inlineformset_factory

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_price', 'payment_method']

OrderItemFormSet = inlineformset_factory(Order, OrderItem, 
                                         form=forms.ModelForm,
                                         fields=['product', 'quantity'],  # Using product ForeignKey
                                         extra=1, can_delete=True)
