from django.urls import path
from . import views

app_name = 'pdv'

urlpatterns = [
    path('', views.PDVView.as_view(), name='pdv'),
    path('search-product/', views.pdv_search_product, name='search_product'),
    path('print-receipt/<int:pk>/', views.print_receipt, name='print_receipt'),
]