from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views
from product.api.viewset import BrandModelViewSet, CategoryModelViewSet, ProductModelViewSet
from product import ultils

app_name ='product'

router = DefaultRouter()
router.register(r'brands', BrandModelViewSet, basename='brands')
router.register(r'categories', CategoryModelViewSet, basename='categories')
router.register(r'products', ProductModelViewSet,  basename='products')

product_urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('update/<int:pk>/', views.product_update, name='update'),
    path('detail/<int:pk>/', views.product_detail, name='detail'),
    path('delete/<int:pk>/', views.product_delete, name='delete'),
    path('valid/', views.product_valid_create, name='valid'),
    path('csv/', ultils.export_products_csv, name='csv'),
    path('excel/', ultils.export_product_excel, name='excel'),
    path('print/', ultils.product_print, name='print'),
    # URLs para NCM
    path('ncm/list/', views.ncm_list, name='ncm_list'),
    path('ncm/create/', views.ncm_create, name='ncm_create'),
    path('ncm/update/<int:pk>/', views.ncm_update, name='ncm_update'),
    path('ncm/delete/<int:pk>/', views.ncm_delete, name='ncm_delete'),
    # URLs para CFOP
    path('cfop/list/', views.cfop_list, name='cfop_list'),
    path('cfop/create/', views.cfop_create, name='cfop_create'),
    path('cfop/update/<int:pk>/', views.cfop_update, name='cfop_update'),
    path('cfop/delete/<int:pk>/', views.cfop_delete, name='cfop_delete'),
    # URLs para TaxBenefit
    path('taxbenefit/list/', views.taxbenefit_list, name='taxbenefit_list'),
    path('taxbenefit/create/', views.taxbenefit_create, name='taxbenefit_create'),
    path('taxbenefit/update/<int:pk>/', views.taxbenefit_update, name='taxbenefit_update'),
    path('taxbenefit/delete/<int:pk>/', views.taxbenefit_delete, name='taxbenefit_delete'),
    # URLs para ExemptionReason
    path('exemptionreason/list/', views.exemptionreason_list, name='exemptionreason_list'),
    path('exemptionreason/create/', views.exemptionreason_create, name='exemptionreason_create'),
    path('exemptionreason/update/<int:pk>/', views.exemptionreason_update, name='exemptionreason_update'),
    path('exemptionreason/delete/<int:pk>/', views.exemptionreason_delete, name='exemptionreason_delete'),
    # URLs para Brand
    path('brand/list/', views.brand_list, name='brand_list'),
    path('brand/create/', views.brand_create, name='brand_create'),
    path('brand/update/<int:pk>/', views.brand_update, name='brand_update'),
    path('brand/delete/<int:pk>/', views.brand_delete, name='brand_delete'),
    # URLs para Category
    path('category/list/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/update/<int:pk>/', views.category_update, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),

]
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', include(product_urlpatterns)),


]