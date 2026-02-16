from django.db import models
from django.conf import settings
from pdv.models import Sale
from order.models import Order

class TransactionType(models.Model):
    """Modelo para tipos de transação"""
    TRANSACTION_TYPE_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('transferencia', 'Transferência'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='Nome')
    description = models.CharField(max_length=255, verbose_name='Descrição', blank=True)
    type_category = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Categoria'
    )
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Tipo de Transação'
        verbose_name_plural = 'Tipos de Transação'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_category_display()})"


class CashBook(models.Model):
    """Modelo para livro caixa"""
    name = models.CharField(max_length=100, verbose_name='Nome do Livro Caixa')
    description = models.CharField(max_length=255, verbose_name='Descrição', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Saldo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Livro Caixa'
        verbose_name_plural = 'Livros Caixa'
        ordering = ['-created_at']

    def __str__(self):
        return f"Livro Caixa: {self.name}"
    
    def calculate_balance(self):
        """Calcular saldo com base nas transações financeiras associadas"""
        from django.db.models import Sum, F
        from django.db.models.functions import Coalesce
        
        # Calcular o saldo somando todas as transações associadas a este livro caixa
        total_transactions = FinancialTransaction.objects.filter(
            cash_book=self
        ).aggregate(
            total=Coalesce(Sum('amount'), 0)
        )['total'] or 0
        
        return total_transactions


class CashRegister(models.Model):
    """Modelo para controle de caixa"""
    opening_date = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora de Abertura')
    closing_date = models.DateTimeField(null=True, blank=True, verbose_name='Data/Hora de Fechamento')
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Saldo Inicial')
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Saldo Final')
    is_open = models.BooleanField(default=True, verbose_name='Caixa Aberto')
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Responsável'
    )
    cash_book = models.ForeignKey(
        CashBook,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Livro Caixa Associado'
    )

    class Meta:
        verbose_name = 'Caixa'
        verbose_name_plural = 'Caixas'
        ordering = ['-opening_date']

    def __str__(self):
        status = "Aberto" if self.is_open else "Fechado"
        return f"Caixa #{self.id} - {status}"


class FinancialTransaction(models.Model):
    """Modelo para transações financeiras"""
    PAYMENT_METHODS = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]

    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name='Tipo de Transação'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name='Método de Pagamento'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    description = models.CharField(max_length=255, verbose_name='Descrição')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')
    cash_book = models.ForeignKey(
        CashBook,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Livro Caixa'
    )
    cash_register = models.ForeignKey(
        CashRegister,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Caixa'
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Venda'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Pedido'
    )
    is_paid = models.BooleanField(default=False, verbose_name='Pago')

    class Meta:
        verbose_name = 'Transação Financeira'
        verbose_name_plural = 'Transações Financeiras'
        ordering = ['-date']

    def __str__(self):
        return f"{self.transaction_type.name} - R$ {self.amount}"