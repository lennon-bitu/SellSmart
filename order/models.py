from django.db import models
from django.conf import settings
from product.models import Product  # Assumindo que o app de produtos já está implementado

class Order(models.Model):
    PENDING = 'E'
    SHIPPED = 'S'
    PREPARING = 'P'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (PENDING, 'Pendente'),
        (SHIPPED, 'Enviado'),
        (PREPARING, 'Preparando'),
        (COMPLETED, 'Completo'),
    ]
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('dinheiro', 'Dinheiro'),
            ('cartao_credito', 'Cartão de Crédito'),
            ('cartao_debito', 'Cartão de Débito'),
            ('pix', 'PIX'),
            ('boleto', 'Boleto'),
        ],
        default='dinheiro',
        verbose_name='Método de Pagamento'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        ordering = ['-pk']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

    def calculate_total(self):
        from decimal import Decimal
        total = sum(Decimal(str(item.product.price)) * item.quantity for item in self.items.all())
        self.total_price = total
        self.save()
    
    def bill_order(self):
        """Faturar pedido e gerar transações financeiras"""
        from financial_control.models import FinancialTransaction, CashRegister, AccountReceivable
        from django.contrib.auth.models import User
        
        if self.status != 'C':  # Só fatura se estiver completo
            return False
        
        cash_register = CashRegister.objects.filter(is_open=True).first()
        
        if self.payment_method in ['cartao_credito', 'cartao_debito', 'pix', 'boleto']:
            # Para pagamentos eletrônicos, criar conta a receber
            AccountReceivable.objects.create(
                customer=self.customer,
                amount=self.total_price,
                due_date=self.created_at.date(),  # Pode ser ajustado conforme política
                description=f"Pedido #{self.id} - Pagamento via {self.get_payment_method_display()}",
                order=self
            )
        elif self.payment_method == 'dinheiro':
            # Para dinheiro, criar transação direta no caixa
            if cash_register:
                FinancialTransaction.objects.create(
                    transaction_type='sale',
                    payment_method=self.payment_method,
                    amount=self.total_price,
                    description=f"Pedido #{self.id} - Pagamento em dinheiro",
                    cash_register=cash_register,
                    order=self
                )
        
        return True


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_subtotal(self):
        from decimal import Decimal
        return Decimal(str(self.product.price)) * self.quantity


class AccountReceivable(models.Model):
    """Modelo para contas a receber"""
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    due_date = models.DateField(verbose_name='Data de Vencimento')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Data de Emissão')
    description = models.CharField(max_length=255, verbose_name='Descrição')
    is_paid = models.BooleanField(default=False, verbose_name='Pago')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    cash_book = models.ForeignKey(
        'financial_control.CashBook',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Livro Caixa'
    )
    sale = models.ForeignKey(
        'pdv.Sale',
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

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['-issue_date']

    def __str__(self):
        status = "Pago" if self.is_paid else "Pendente"
        return f"Receber R$ {self.amount} - {status}"

    def mark_as_paid(self, cash_book=None):
        """Marcar conta como paga"""
        self.is_paid = True
        self.payment_date = self.issue_date  # ou usar timezone.now() se for o caso
        if cash_book:
            self.cash_book = cash_book
        self.save()
        
        # Registrar transação financeira se for em dinheiro ou se for fornecido um livro caixa
        if cash_book:
            from financial_control.models import FinancialTransaction
            FinancialTransaction.objects.create(
                transaction_type='receivable',
                payment_method='dinheiro',
                amount=self.amount,
                description=f"Pagamento Recebido: {self.description}",
                cash_book=cash_book,
                sale=self.sale,
                order=self.order
            )
        
        return True


class AccountPayable(models.Model):
    """Modelo para contas a pagar"""
    supplier = models.CharField(max_length=255, verbose_name='Fornecedor')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    due_date = models.DateField(verbose_name='Data de Vencimento')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Data de Emissão')
    description = models.CharField(max_length=255, verbose_name='Descrição')
    is_paid = models.BooleanField(default=False, verbose_name='Pago')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    cash_book = models.ForeignKey(
        'financial_control.CashBook',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Livro Caixa'
    )

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['-issue_date']

    def __str__(self):
        status = "Pago" if self.is_paid else "Pendente"
        return f"Pagar R$ {self.amount} - {status}"

    def mark_as_paid(self, cash_book=None):
        """Marcar conta como paga"""
        self.is_paid = True
        self.payment_date = self.issue_date  # ou usar timezone.now() se for o caso
        if cash_book:
            self.cash_book = cash_book
        self.save()
        
        # Registrar transação financeira de saída
        if cash_book:
            from financial_control.models import FinancialTransaction
            FinancialTransaction.objects.create(
                transaction_type='payable',
                payment_method='dinheiro',
                amount=-self.amount,  # Valor negativo para saída
                description=f"Pagamento Efetuado: {self.description}",
                cash_book=cash_book
            )
        
        return True