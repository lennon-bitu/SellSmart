from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from product.models import Product
import json

@method_decorator(login_required, name='dispatch')
class PDVView(View):
    """View principal do PDV"""
    
    def get(self, request):
        # Obter todos os produtos ativos para o autocomplete
        products = Product.objects.filter(is_active=True)
        
        # Criar formulários
        sale_form = SaleForm()
        sale_item_form = SaleItemForm()
        
        context = {
            'sale_form': sale_form,
            'sale_item_form': sale_item_form,
            'products': products,
        }
        return render(request, 'pdv/pdv.html', context)
    
    def post(self, request):
        # Processar dados do carrinho e finalizar venda
        try:
            # Obter dados do POST
            data = json.loads(request.body)
            items_data = data.get('items', [])
            customer_id = data.get('customer_id')
            discount = float(data.get('discount', 0))
            payment_method = data.get('payment_method', 'dinheiro')
            
            # Criar a venda
            sale = Sale.objects.create(
                customer_id=customer_id if customer_id else None,
                discount=discount,
                payment_method=payment_method
            )
            
            # Adicionar itens à venda
            total_amount = 0
            for item_data in items_data:
                product_id = item_data['product_id']
                quantity = int(item_data['quantity'])
                
                product = Product.objects.get(id=product_id)
                
                # Calcular preços
                unit_price = product.price
                total_price = unit_price * quantity
                
                # Criar item de venda
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                
                total_amount += total_price
            
            # Converter para Decimal antes de fazer a operação
            from decimal import Decimal
            from financial_control.models import FinancialTransaction, CashRegister, AccountReceivable
            from django.contrib.auth.models import User
            
            total_amount_decimal = Decimal(str(total_amount))
            discount_decimal = Decimal(str(discount))
            
            # Atualizar valores da venda
            sale.total_amount = total_amount_decimal
            sale.final_amount = total_amount_decimal - discount_decimal
            sale.completed = True
            sale.save()
            
            # Criar transação financeira com base no método de pagamento
            cash_register = CashRegister.objects.filter(is_open=True).first()
            
            if payment_method in ['cartao_credito', 'cartao_debito', 'pix', 'boleto']:
                # Para pagamentos eletrônicos, criar conta a receber
                account_receivable = AccountReceivable.objects.create(
                    customer=sale.customer or User.objects.first(),  # Usar primeiro usuário se não houver cliente
                    amount=sale.final_amount,
                    due_date=sale.created_at.date(),  # Pode ser ajustado conforme política
                    description=f"Venda #{sale.id} - Pagamento via {payment_method}",
                    sale=sale
                )
            elif payment_method == 'dinheiro':
                # Para dinheiro, criar transação direta no caixa
                if cash_register:
                    FinancialTransaction.objects.create(
                        transaction_type='sale',
                        payment_method=payment_method,
                        amount=sale.final_amount,
                        description=f"Venda #{sale.id} - Pagamento em dinheiro",
                        cash_register=cash_register,
                        sale=sale
                    )
            
            return JsonResponse({
                'success': True,
                'sale_id': sale.id,
                'message': f'Venda #{sale.id} registrada com sucesso!',
                'print_url': f'/pdv/print-receipt/{sale.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao processar a venda: {str(e)}'
            })


@login_required
def pdv_search_product(request):
    """Busca produtos para o PDV"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            name__icontains=query,
            is_active=True
        ).values('id', 'name', 'price', 'stock')
        return JsonResponse(list(products), safe=False)
    return JsonResponse([], safe=False)


@login_required
def print_receipt(request, pk):
    """Imprimir recibo de venda"""
    from django.shortcuts import get_object_or_404
    from .models import Sale
    
    sale = get_object_or_404(Sale, pk=pk)
    context = {
        'sale': sale
    }
    return render(request, 'pdv/receipt_print.html', context)