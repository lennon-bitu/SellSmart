import csv
from django.http import HttpResponse
from django.contrib import admin
from product.models import Brand, Category, Product, NCM, CFOP, TaxBenefit, ExemptionReason

# Register your models here.
@admin.register(NCM)
class NcmAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('name','code')
    list_filter = ('is_active',)


@admin.register(CFOP)
class CfopAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('name','code')
    list_filter = ('is_active',)


@admin.register(TaxBenefit)
class TaxBenefitAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('name','code')
    list_filter = ('is_active',)


@admin.register(ExemptionReason)
class ExemptionReasonAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('name','code')
    list_filter = ('is_active',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category','cost_price', 'price', 'profit_margin',
    'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'brand__name', 'category__name')
    list_filter = ('is_active', 'brand', 'category')

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['título', 'marca', 'categoria', 'preço','ativo', 'descrição', 'criado em', 'atualizado em'])
        for product in queryset:
            writer.writerow([product.title, product.brand.name, product.category.name,
            product.price, product.is_active, product.description,
            product.created_at, product.updated_at])
                
        return response
    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]