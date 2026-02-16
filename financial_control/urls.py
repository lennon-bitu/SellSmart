from django.urls import path
from . import views

app_name = 'financial_control'

urlpatterns = [
    path('', views.FinancialControlView.as_view(), name='financial_control'),
    path('open-cash-register/', views.open_cash_register, name='open_cash_register'),
    path('close-cash-register/<int:pk>/', views.close_cash_register, name='close_cash_register'),
    path('cash-out/', views.cash_out, name='cash_out'),
    path('cash-in/', views.cash_in, name='cash_in'),
    path('create-account-receivable/', views.create_account_receivable, name='create_account_receivable'),
    path('create-account-payable/', views.create_account_payable, name='create_account_payable'),
    path('mark-as-paid-receivable/<int:pk>/', views.mark_as_paid_receivable, name='mark_as_paid_receivable'),
    path('mark-as-paid-payable/<int:pk>/', views.mark_as_paid_payable, name='mark_as_paid_payable'),
    
    # Novas funcionalidades
    path('cash-books/', views.cash_book_list, name='cash_book_list'),
    path('cash-books/create/', views.create_cash_book, name='create_cash_book'),
    path('cash-books/<int:pk>/', views.cash_book_detail, name='cash_book_detail'),
    path('accounts-receivable/', views.account_receivable_list, name='account_receivable_list'),
    path('accounts-payable/', views.account_payable_list, name='account_payable_list'),
    path('transfer/', views.transfer_between_cash_books, name='transfer'),
    path('manual-entry/', views.manual_entry, name='manual_entry'),
    path('manual-entry-list/', views.manual_entry_list, name='manual_entry_list'),
    path('mark-as-paid-receivable-with-cash-book/<int:pk>/', views.mark_as_paid_receivable_with_cash_book, name='mark_as_paid_receivable_with_cash_book'),
    path('mark-as-paid-payable-with-cash-book/<int:pk>/', views.mark_as_paid_payable_with_cash_book, name='mark_as_paid_payable_with_cash_book'),
    path('reverse-transaction/<int:pk>/', views.reverse_transaction, name='reverse_transaction'),
    
    # Funcionalidades de editar e excluir
    path('edit-account-receivable/<int:pk>/', views.edit_account_receivable, name='edit_account_receivable'),
    path('delete-account-receivable/<int:pk>/', views.delete_account_receivable, name='delete_account_receivable'),
    path('edit-account-payable/<int:pk>/', views.edit_account_payable, name='edit_account_payable'),
    path('delete-account-payable/<int:pk>/', views.delete_account_payable, name='delete_account_payable'),
    
    # URLs para tipos de transação
    path('transaction-types/', views.transaction_type_list, name='transaction_type_list'),
    path('transaction-types/create/', views.transaction_type_create, name='transaction_type_create'),
    path('transaction-types/update/<int:pk>/', views.transaction_type_update, name='transaction_type_update'),
    path('transaction-types/delete/<int:pk>/', views.transaction_type_delete, name='transaction_type_delete'),
]