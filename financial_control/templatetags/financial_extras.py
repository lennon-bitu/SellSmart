from django import template

register = template.Library()

@register.filter
def abs_value(value):
    """Retorna o valor absoluto de um número"""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return 0

@register.simple_tag
def calculate_running_balance(transactions, index):
    """Calcula o saldo acumulado até um determinado índice de transação"""
    balance = 0
    for i, transaction in enumerate(transactions):
        if i <= index:
            balance += transaction.amount
    return balance