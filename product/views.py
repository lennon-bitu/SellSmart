from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from product.models import   Product
from product.forms import ProductForm

# Create your views here.


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

def product_create(request):

    create_form_data = request.session.get('create_form_data', None)
    form = ProductForm(create_form_data, )
    products = Product.objects.all()

    return render(request, 'product/product_list.html', {'form': form, 'products':products})


def product_valid_create(request):

    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['create_form_data'] = POST
    form = ProductForm(POST)

    if form.is_valid(): 
        form.save()
        messages.success(request, 'Produto cadastrado com Sucesso!')
        #fazemos a limpeza da sessão de criação do formulario
        del(request.session['create_form_data'])

    return redirect('product:create')