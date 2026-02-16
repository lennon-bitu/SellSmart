from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View

from product.models import Product
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from .forms import OrderForm, OrderItemFormSet

class OrderListView(View):
    def get(self, request):
        from django.core.paginator import Paginator
        
        # Obter parâmetros de filtro
        status_filter = request.GET.get('status')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Filtrar pedidos
        orders = Order.objects.all().order_by('-created_at')
        
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        if start_date:
            from datetime import datetime
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__gte=start_date_obj)
        
        if end_date:
            from datetime import datetime
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__lte=end_date_obj)
        
        # Paginação
        paginator = Paginator(orders, 25)  # 25 resultados por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        current_filters = {
            'status_filter': status_filter,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'orders/order_list.html', {
            'page_obj': page_obj,
            'current_filters': current_filters
        })

class OrderCreateView(View):
    def get(self, request):
        order_form = OrderForm()
        order_item_form = OrderItemForm()
        return render(request, 'orders/order_form.html', {
            'order_form': order_form,
            'order_item_form': order_item_form
        })

    def post(self, request):
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)
        
        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = request.user
            order.save()

            order_item = order_item_form.save(commit=False)
            order_item.order = order
            order_item.save()
            
            order.calculate_total()

            return redirect('orders:order_list')
        return render(request, 'orders/order_form.html', {
            'order_form': order_form,
            'order_item_form': order_item_form
        })


def create_order(request):
    from django.contrib.auth.models import User
    products = Product.objects.all()
    customers = User.objects.all()  # Obter todos os clientes
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        status = request.POST.get('status', 'E')  # Valor padrão é Pendente
        total_price = request.POST.get('total_price', 0.00)
        
        customer = User.objects.get(id=customer_id)
        
        # Criar o pedido
        order = Order.objects.create(
            customer=customer,
            status=status,
            total_price=total_price
        )
        
        # Processar itens do pedido
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        
        for i in range(len(product_ids)):
            product_id = product_ids[i]
            quantity = int(quantities[i])
            
            if product_id and quantity:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
        
        order.calculate_total()  # Recalcular o total baseado nos itens
        
        messages.success(request, f'Pedido #{order.id} criado com sucesso!')
        return redirect('orders:order_list')

    context = {
        'products': products,
        'customers': customers,
    }
    return render(request, 'orders/order_form.html', context)



class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, customer=request.user)
        return render(request, 'orders/order_detail.html', {'order': order})


def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_payment_method = request.POST.get('payment_method')
        
        if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
            order.status = new_status
            if new_payment_method:
                order.payment_method = new_payment_method
            order.save()
            
            # Se o status for completado e o pagamento não for em dinheiro, criar conta a receber
            if order.status == 'C' and order.payment_method in ['cartao_credito', 'cartao_debito', 'pix', 'boleto']:
                from financial_control.models import AccountReceivable
                from django.contrib.auth.models import User
                AccountReceivable.objects.create(
                    customer=order.customer,
                    amount=order.total_price,
                    due_date=order.created_at.date(),
                    description=f"Pedido #{order.id} - Pagamento via {order.get_payment_method_display()}",
                    order=order
                )
            
            messages.success(request, f'Status do pedido #{order.id} atualizado com sucesso!')
        else:
            messages.error(request, 'Status inválido.')
        return redirect('orders:order_list')
    return render(request, 'orders/order_update_status.html', {'order': order})
