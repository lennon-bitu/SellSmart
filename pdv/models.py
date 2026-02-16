from django.db import models
from django.conf import settings
from product.models import Product

class Sale(models.Model):
    """Modelo para representar uma venda no PDV"""
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Cliente'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Valor Total'
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Desconto'
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Valor Final'
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
        verbose_name='Método de Pagamento'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')
    completed = models.BooleanField(default=False, verbose_name='Completada')

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-created_at']

    def __str__(self):
        return f"Venda #{self.id} - R$ {self.final_amount}"


class SaleItem(models.Model):
    """Modelo para representar um item de venda"""
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE, verbose_name='Venda')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Total')

    class Meta:
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def calculate_total(self):
        """Calcula o preço total do item (quantidade * preço unitário)"""
        from decimal import Decimal
        return Decimal(str(self.unit_price)) * Decimal(str(self.quantity))
