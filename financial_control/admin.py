from django.contrib import admin
from .models import CashBook, CashRegister, FinancialTransaction
from order.models import AccountReceivable, AccountPayable

@admin.register(CashBook)
class CashBookAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ['id', 'opening_date', 'closing_date', 'opening_balance', 'closing_balance', 'is_open', 'responsible', 'cash_book']
    list_filter = ['is_open', 'opening_date', 'responsible', 'cash_book']
    search_fields = ['id', 'responsible__username']

@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'payment_method', 'amount', 'date', 'cash_book', 'cash_register', 'sale', 'order']
    list_filter = ['transaction_type', 'payment_method', 'date', 'cash_book', 'cash_register']
    search_fields = ['description', 'sale__id', 'order__id']

@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'due_date', 'is_paid', 'cash_book', 'sale', 'order']
    list_filter = ['is_paid', 'due_date', 'issue_date', 'cash_book']
    search_fields = ['customer__username', 'description', 'sale__id', 'order__id']

@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'amount', 'due_date', 'is_paid', 'cash_book']
    list_filter = ['is_paid', 'due_date', 'issue_date', 'cash_book']
    search_fields = ['supplier', 'description']