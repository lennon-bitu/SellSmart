from django.contrib import admin
from .models import Sale, SaleItem

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'discount', 'final_amount', 'payment_method', 'created_at', 'completed']
    list_filter = ['payment_method', 'completed', 'created_at']
    search_fields = ['id', 'customer__username']
    readonly_fields = ['created_at']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['sale__id', 'product__name']