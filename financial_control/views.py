from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
from .models import CashBook, CashRegister, FinancialTransaction, TransactionType
from order.models import AccountReceivable, AccountPayable
from .forms import CashBookForm, CashRegisterOpeningForm, CashOutForm, CashInForm, AccountReceivableForm, AccountPayableForm, ManualEntryForm, TransactionTypeForm

@method_decorator(login_required, name='dispatch')
class FinancialControlView(View):
    """View principal do controle financeiro"""
    
    def get(self, request):
        cash_books = CashBook.objects.filter(is_active=True)
        cash_registers = CashRegister.objects.filter(is_open=True)
        transactions = FinancialTransaction.objects.all().order_by('-date')[:10]  # Úimas 10 transações
        receivables = AccountReceivable.objects.filter(is_paid=False).order_by('due_date')[:10]  # Úimas 10 contas a receber
        payables = AccountPayable.objects.filter(is_paid=False).order_by('due_date')[:10]  # Úimas 10 contas a pagar
        
        context = {
            'cash_books': cash_books,
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


@login_required
def cash_book_list(request):
    """Lista de livros caixa"""
    cash_books = CashBook.objects.all()
    paginator = Paginator(cash_books, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'financial_control/cash_book_list.html', context)


@login_required
def create_cash_book(request):
    """Criar livro caixa"""
    if request.method == 'POST':
        form = CashBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro caixa criado com sucesso!')
            return redirect('financial_control:cash_book_list')
    else:
        form = CashBookForm()
    
    context = {
        'form': form,
        'action': 'Novo Livro Caixa'
    }
    return render(request, 'financial_control/cash_book_form.html', context)


@login_required
def cash_book_detail(request, pk):
    """Detalhes do livro caixa"""
    cash_book = get_object_or_404(CashBook, pk=pk)
    transactions = FinancialTransaction.objects.filter(cash_book=cash_book).order_by('-date')
    
    # Paginação
    paginator = Paginator(transactions, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cash_book': cash_book,
        'page_obj': page_obj
    }
    return render(request, 'financial_control/cash_book_detail.html', context)


@login_required
def account_receivable_list(request):
    """Lista de contas a receber com filtros e paginação"""
    is_paid = request.GET.get('is_paid')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    accounts = AccountReceivable.objects.all()
    
    if is_paid is not None:
        if is_paid == 'true':
            accounts = accounts.filter(is_paid=True)
        elif is_paid == 'false':
            accounts = accounts.filter(is_paid=False)
    
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        accounts = accounts.filter(issue_date__gte=start_date_obj)
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        accounts = accounts.filter(issue_date__lte=end_date_obj)
    
    # Paginação
    paginator = Paginator(accounts, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_filters': {
            'is_paid': is_paid,
            'start_date': start_date,
            'end_date': end_date,
        }
    }
    return render(request, 'financial_control/account_receivable_list.html', context)


@login_required
def account_payable_list(request):
    """Lista de contas a pagar com filtros e paginação"""
    is_paid = request.GET.get('is_paid')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    accounts = AccountPayable.objects.all()
    
    if is_paid is not None:
        if is_paid == 'true':
            accounts = accounts.filter(is_paid=True)
        elif is_paid == 'false':
            accounts = accounts.filter(is_paid=False)
    
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        accounts = accounts.filter(issue_date__gte=start_date_obj)
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        accounts = accounts.filter(issue_date__lte=end_date_obj)
    
    # Paginação
    paginator = Paginator(accounts, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_filters': {
            'is_paid': is_paid,
            'start_date': start_date,
            'end_date': end_date,
        }
    }
    return render(request, 'financial_control/account_payable_list.html', context)


@login_required
def transfer_between_cash_books(request):
    """Transferência entre livros caixa"""
    from .forms import TransferForm
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save()
            if transfer.execute_transfer():
                messages.success(request, 'Transferência realizada com sucesso!')
            else:
                messages.error(request, 'Erro ao realizar transferência!')
            return redirect('financial_control:financial_control')
    else:
        form = TransferForm()
    
    context = {
        'form': form,
        'action': 'Nova Transferência'
    }
    return render(request, 'financial_control/transfer_form.html', context)


@login_required
def manual_entry(request):
    """Lançamento manual no livro caixa"""
    if request.method == 'POST':
        form = ManualEntryForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, 'Lançamento realizado com sucesso!')
            return redirect('financial_control:manual_entry_list')
    else:
        form = ManualEntryForm()
    
    context = {
        'form': form,
        'action': 'Novo Lançamento Manual'
    }
    return render(request, 'financial_control/manual_entry_form.html', context)


@login_required
def manual_entry_list(request):
    """Lista de lançamentos manuais com filtros e paginação"""
    # Obter parâmetros de filtro
    cash_book_filter = request.GET.get('cash_book')
    transaction_type_filter = request.GET.get('transaction_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filtrar lançamentos
    entries = FinancialTransaction.objects.all().order_by('-date')
    
    if cash_book_filter:
        entries = entries.filter(cash_book__id=cash_book_filter)
    
    if transaction_type_filter:
        entries = entries.filter(transaction_type__id=transaction_type_filter)
    
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        entries = entries.filter(date__date__gte=start_date_obj)
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        entries = entries.filter(date__date__lte=end_date_obj)
    
    # Paginação
    paginator = Paginator(entries, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obter opções para filtros
    cash_books = CashBook.objects.all()
    transaction_types = TransactionType.objects.all()
    
    current_filters = {
        'cash_book_filter': cash_book_filter,
        'transaction_type_filter': transaction_type_filter,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    context = {
        'page_obj': page_obj,
        'cash_books': cash_books,
        'transaction_types': transaction_types,
        'current_filters': current_filters
    }
    return render(request, 'financial_control/manual_entry_list.html', context)


@login_required
def mark_as_paid_receivable_with_cash_book(request, pk):
    """Marcar conta a receber como paga com seleção de livro caixa"""
    account = get_object_or_404(AccountReceivable, pk=pk)
    
    if request.method == 'POST':
        cash_book_id = request.POST.get('cash_book')
        cash_book = get_object_or_404(CashBook, pk=cash_book_id)
        
        if account.mark_as_paid(cash_book):
            messages.success(request, 'Conta marcada como paga e registrada no livro caixa!')
        else:
            messages.error(request, 'Erro ao marcar conta como paga!')
        
        return redirect('financial_control:account_receivable_list')
    
    cash_books = CashBook.objects.filter(is_active=True)
    context = {
        'account': account,
        'cash_books': cash_books
    }
    return render(request, 'financial_control/select_cash_book.html', context)


@login_required
def mark_as_paid_payable_with_cash_book(request, pk):
    """Marcar conta a pagar como paga com seleção de livro caixa"""
    account = get_object_or_404(AccountPayable, pk=pk)
    
    if request.method == 'POST':
        cash_book_id = request.POST.get('cash_book')
        cash_book = get_object_or_404(CashBook, pk=cash_book_id)
        
        if account.mark_as_paid(cash_book):
            messages.success(request, 'Conta marcada como paga e registrada no livro caixa!')
        else:
            messages.error(request, 'Erro ao marcar conta como paga!')
        
        return redirect('financial_control:account_payable_list')
    
    cash_books = CashBook.objects.filter(is_active=True)
    context = {
        'account': account,
        'cash_books': cash_books
    }
    return render(request, 'financial_control/select_cash_book.html', context)


@login_required
def reverse_transaction(request, pk):
    """Estornar ou excluir uma transação"""
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'reverse':
            # Criar transação inversa
            reverse_transaction = FinancialTransaction.objects.create(
                transaction_type=transaction.transaction_type,
                payment_method=transaction.payment_method,
                amount=-transaction.amount,  # Valor oposto
                description=f"ESTORNO: {transaction.description}",
                cash_book=transaction.cash_book,
                cash_register=transaction.cash_register,
                sale=transaction.sale,
                order=transaction.order
            )
            messages.success(request, 'Transação estornada com sucesso!')
        elif action == 'delete':
            transaction.delete()
            messages.success(request, 'Transação excluída com sucesso!')
        
        return redirect('financial_control:financial_control')
    
    context = {
        'transaction': transaction
    }
    return render(request, 'financial_control/reverse_transaction.html', context)


@login_required
def edit_account_receivable(request, pk):
    """Editar conta a receber"""
    account = get_object_or_404(AccountReceivable, pk=pk)
    
    if request.method == 'POST':
        form = AccountReceivableForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta a receber atualizada com sucesso!')
            return redirect('financial_control:account_receivable_list')
    else:
        form = AccountReceivableForm(instance=account)
    
    context = {
        'form': form,
        'action': 'Editar Conta a Receber',
        'account': account
    }
    return render(request, 'financial_control/account_form.html', context)


@login_required
def delete_account_receivable(request, pk):
    """Excluir conta a receber"""
    account = get_object_or_404(AccountReceivable, pk=pk)
    
    if request.method == 'POST':
        account_id = account.id  # Guardar o ID antes de excluir
        account.delete()
        messages.success(request, f'Conta a receber #{account_id} excluída com sucesso!')
        return redirect('financial_control:account_receivable_list')
    
    context = {
        'account': account,
        'type': 'receivable'
    }
    return render(request, 'financial_control/delete_confirmation.html', context)


@login_required
def edit_account_payable(request, pk):
    """Editar conta a pagar"""
    account = get_object_or_404(AccountPayable, pk=pk)
    
    if request.method == 'POST':
        form = AccountPayableForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta a pagar atualizada com sucesso!')
            return redirect('financial_control:account_payable_list')
    else:
        form = AccountPayableForm(instance=account)
    
    context = {
        'form': form,
        'action': 'Editar Conta a Pagar',
        'account': account
    }
    return render(request, 'financial_control/account_form.html', context)


@login_required
def delete_account_payable(request, pk):
    """Excluir conta a pagar"""
    account = get_object_or_404(AccountPayable, pk=pk)
    
    if request.method == 'POST':
        account_id = account.id  # Guardar o ID antes de excluir
        account.delete()
        messages.success(request, f'Conta a pagar #{account_id} excluída com sucesso!')
        return redirect('financial_control:account_payable_list')
    
    context = {
        'account': account,
        'type': 'payable'
    }
    return render(request, 'financial_control/delete_confirmation.html', context)


@login_required
def transaction_type_list(request):
    """Lista de tipos de transação"""
    transaction_types = TransactionType.objects.all()
    paginator = Paginator(transaction_types, 25)  # 25 resultados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    return render(request, 'financial_control/transaction_type_list.html', context)


@login_required
def transaction_type_create(request):
    """Criar tipo de transação"""
    from .forms import TransactionTypeForm
    if request.method == 'POST':
        form = TransactionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de transação criado com sucesso!')
            return redirect('financial_control:transaction_type_list')
    else:
        form = TransactionTypeForm()
    
    context = {
        'form': form,
        'action': 'Novo Tipo de Transação'
    }
    return render(request, 'financial_control/transaction_type_form.html', context)


@login_required
def transaction_type_update(request, pk):
    """Atualizar tipo de transação"""
    from .forms import TransactionTypeForm
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    
    if request.method == 'POST':
        form = TransactionTypeForm(request.POST, instance=transaction_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de transação atualizado com sucesso!')
            return redirect('financial_control:transaction_type_list')
    else:
        form = TransactionTypeForm(instance=transaction_type)
    
    context = {
        'form': form,
        'action': 'Editar Tipo de Transação',
        'transaction_type': transaction_type
    }
    return render(request, 'financial_control/transaction_type_form.html', context)


@login_required
def transaction_type_delete(request, pk):
    """Excluir tipo de transação"""
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    
    if request.method == 'POST':
        transaction_type.delete()
        messages.success(request, f'Tipo de transação "{transaction_type.name}" excluído com sucesso!')
        return redirect('financial_control:transaction_type_list')
    
    context = {
        'transaction_type': transaction_type
    }
    return render(request, 'financial_control/transaction_type_confirm_delete.html', context)


@login_required
def order_update_status(request, pk):
    """Atualizar status de pedido"""
    from order.models import Order
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['E', 'P', 'S', 'C']:  # Validação básica dos status
            order.status = new_status
            order.save()
            messages.success(request, f'Status do pedido #{order.id} atualizado com sucesso!')
        else:
            messages.error(request, 'Status inválido.')
        return redirect('orders:order_list')
    
    context = {
        'order': order
    }
    return render(request, 'orders/order_update_status.html', context)