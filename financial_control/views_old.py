from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from .models import CashRegister, FinancialTransaction, AccountReceivable, AccountPayable
from .forms import CashRegisterOpeningForm, CashOutForm, CashInForm, AccountReceivableForm, AccountPayableForm
from pdv.models import Sale
from order.models import Order
from django.contrib.auth.models import User

@method_decorator(login_required, name='dispatch')
class FinancialControlView(View):
    """View principal do controle financeiro"""
    
    def get(self, request):
        cash_registers = CashRegister.objects.filter(is_open=True)
        transactions = FinancialTransaction.objects.all()[:10]  # Úimas 10 transações
        receivables = AccountReceivable.objects.filter(is_paid=False)[:10]  # Úimas 10 contas a receber
        payables = AccountPayable.objects.filter(is_paid=False)[:10]  # Úimas 10 contas a pagar
        
        context = {
            'cash_registers': cash_registers,
            'transactions': transactions,
            'receivables': receivables,
            'payables': payables,
        }
        return render(request, 'financial_control/financial_control.html', context)


@login_required
def open_cash_register(request):
    """Abrir caixa"""
    if request.method == 'POST':
        form = CashRegisterOpeningForm(request.POST)
        if form.is_valid():
            cash_register = form.save(commit=False)
            cash_register.responsible = request.user
            cash_register.save()
            messages.success(request, 'Caixa aberto com sucesso!')
            return redirect('financial_control:financial_control')
    else:
        form = CashRegisterOpeningForm()
    
    context = {
        'form': form,
        'action': 'Abrir Caixa'
    }
    return render(request, 'financial_control/cash_register_form.html', context)


@login_required
def close_cash_register(request, pk):
    """Fechar caixa"""
    cash_register = get_object_or_404(CashRegister, pk=pk)
    cash_register.is_open = False
    cash_register.save()
    messages.success(request, 'Caixa fechado com sucesso!')
    return redirect('financial_control:financial_control')


@login_required
def cash_out(request):
    """Sangria de caixa"""
    if request.method == 'POST':
        form = CashOutForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'cash_out'
            transaction.payment_method = 'dinheiro'
            transaction.cash_register = CashRegister.objects.filter(is_open=True).first()
            transaction.description = f"Sangria: {transaction.description}"
            transaction.save()
            messages.success(request, 'Sangria realizada com sucesso!')
            return redirect('financial_control:financial_control')
    else:
        form = CashOutForm()
    
    context = {
        'form': form,
        'action': 'Sangria de Caixa'
    }
    return render(request, 'financial_control/transaction_form.html', context)


@login_required
def cash_in(request):
    """Suprimento de caixa"""
    if request.method == 'POST':
        form = CashInForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'cash_in'
            transaction.payment_method = 'dinheiro'
            transaction.cash_register = CashRegister.objects.filter(is_open=True).first()
            transaction.description = f"Suprimento: {transaction.description}"
            transaction.save()
            messages.success(request, 'Suprimento realizado com sucesso!')
            return redirect('financial_control:financial_control')
    else:
        form = CashInForm()
    
    context = {
        'form': form,
        'action': 'Suprimento de Caixa'
    }
    return render(request, 'financial_control/transaction_form.html', context)


@login_required
def create_account_receivable(request):
    """Criar conta a receber"""
    if request.method == 'POST':
        form = AccountReceivableForm(request.POST)
        if form.is_valid():
            account = form.save()
            # Criar transação financeira associada
            FinancialTransaction.objects.create(
                transaction_type='receivable',
                payment_method=form.cleaned_data['sale'].payment_method if form.cleaned_data['sale'] else 'boleto',
                amount=account.amount,
                description=f"Conta a Receber: {account.description}",
                cash_register=CashRegister.objects.filter(is_open=True).first(),
                sale=form.cleaned_data['sale'],
                order=form.cleaned_data['order']
            )
            messages.success(request, 'Conta a receber criada com sucesso!')
            return redirect('financial_control:financial_control')
    else:
        form = AccountReceivableForm()
    
    context = {
        'form': form,
        'action': 'Nova Conta a Receber'
    }
    return render(request, 'financial_control/account_form.html', context)


@login_required
def create_account_payable(request):
    """Criar conta a pagar"""
    if request.method == 'POST':
        form = AccountPayableForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Conta a pagar criada com sucesso!')
            return redirect('financial_control:financial_control')
    else:
        form = AccountPayableForm()
    
    context = {
        'form': form,
        'action': 'Nova Conta a Pagar'
    }
    return render(request, 'financial_control/account_form.html', context)


@login_required
def mark_as_paid_receivable(request, pk):
    """Marcar conta a receber como paga"""
    account = get_object_or_404(AccountReceivable, pk=pk)
    account.is_paid = True
    account.payment_date = account.issue_date  # ou usar timezone.now() se for o caso
    account.save()
    
    # Criar transação financeira para entrada em caixa se for dinheiro
    if hasattr(account, 'sale') and account.sale and account.sale.payment_method == 'dinheiro':
        cash_register = CashRegister.objects.filter(is_open=True).first()
        if cash_register:
            FinancialTransaction.objects.create(
                transaction_type='sale',
                payment_method='dinheiro',
                amount=account.amount,
                description=f"Pagamento Recebido: {account.description}",
                cash_register=cash_register,
                sale=account.sale
            )
    
    messages.success(request, 'Conta marcada como paga!')
    return redirect('financial_control:financial_control')


@login_required
def mark_as_paid_payable(request, pk):
    """Marcar conta a pagar como paga"""
    account = get_object_or_404(AccountPayable, pk=pk)
    account.is_paid = True
    account.payment_date = account.issue_date  # ou usar timezone.now() se for o caso
    account.save()
    
    # Criar transação financeira para saída de caixa
    cash_register = CashRegister.objects.filter(is_open=True).first()
    if cash_register:
        FinancialTransaction.objects.create(
            transaction_type='payable',
            payment_method='dinheiro',
            amount=-account.amount,  # Valor negativo para saída
            description=f"Pagamento Efetuado: {account.description}",
            cash_register=cash_register
        )
    
    messages.success(request, 'Conta marcada como paga!')
    return redirect('financial_control:financial_control')


# Exportar todas as funções antigas
__all__ = [
    'FinancialControlView', 'open_cash_register', 'close_cash_register', 
    'cash_out', 'cash_in', 'create_account_receivable', 'create_account_payable',
    'mark_as_paid_receivable', 'mark_as_paid_payable'
]