from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from order.models import Order
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione a lista de orders ao contexto, verificando se o cliente existe
        try:
            # Usar prefetch_related para otimizar o acesso aos clientes
            context['orders'] = Order.objects.prefetch_related('customer').all()
        except Exception as e:
            # Em caso de erro, retornar uma lista vazia
            context['orders'] = []
            print(f"Erro ao carregar pedidos: {e}")
        return context


class AnalyticView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/analytic.html"