from django import forms
from .models import CashBook, CashRegister, FinancialTransaction, TransactionType
from order.models import AccountReceivable, AccountPayable

class TransactionTypeForm(forms.ModelForm):
    """Formulário para tipos de transação"""
    class Meta:
        model = TransactionType
        fields = ['name', 'description', 'type_category', 'is_active']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'type_category': 'Categoria',
            'is_active': 'Ativo'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type_category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ManualEntryForm(forms.ModelForm):
    """Formulário para lançamentos manuais"""
    class Meta:
        model = FinancialTransaction
        fields = ['transaction_type', 'payment_method', 'amount', 'description', 'cash_book']
        labels = {
            'transaction_type': 'Tipo de Transação',
            'payment_method': 'Método de Pagamento',
            'amount': 'Valor',
            'description': 'Descrição',
            'cash_book': 'Livro Caixa'
        }
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'cash_book': forms.Select(attrs={'class': 'form-control'})
        }


class CashBookForm(forms.ModelForm):
    """Formulário para livro caixa"""
    class Meta:
        model = CashBook
        fields = ['name', 'description', 'is_active']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'is_active': 'Ativo'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class CashRegisterOpeningForm(forms.ModelForm):
    """Formulário para abertura de caixa"""
    class Meta:
        model = CashRegister
        fields = ['opening_balance', 'cash_book']
        labels = {
            'opening_balance': 'Saldo Inicial',
            'cash_book': 'Livro Caixa'
        }
        widgets = {
            'opening_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cash_book': forms.Select(attrs={'class': 'form-control'})
        }


class CashOutForm(forms.Form):
    """Formulário para sangria de caixa"""
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Valor'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Descrição',
        max_length=255
    )


class CashInForm(forms.Form):
    """Formulário para suprimento de caixa"""
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Valor'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Descrição',
        max_length=255
    )


class AccountReceivableForm(forms.ModelForm):
    """Formulário para contas a receber"""
    class Meta:
        model = AccountReceivable
        fields = ['customer', 'amount', 'due_date', 'description', 'sale', 'order', 'cash_book']
        labels = {
            'customer': 'Cliente',
            'amount': 'Valor',
            'due_date': 'Data de Vencimento',
            'description': 'Descrição',
            'sale': 'Venda',
            'order': 'Pedido',
            'cash_book': 'Livro Caixa'
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'cash_book': forms.Select(attrs={'class': 'form-control'}),
        }


class AccountPayableForm(forms.ModelForm):
    """Formulário para contas a pagar"""
    class Meta:
        model = AccountPayable
        fields = ['supplier', 'amount', 'due_date', 'description', 'cash_book']
        labels = {
            'supplier': 'Fornecedor',
            'amount': 'Valor',
            'due_date': 'Data de Vencimento',
            'description': 'Descrição',
            'cash_book': 'Livro Caixa'
        }
        widgets = {
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'cash_book': forms.Select(attrs={'class': 'form-control'}),
        }