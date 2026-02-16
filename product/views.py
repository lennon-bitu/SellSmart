from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from product.models import   Product, NCM, CFOP, TaxBenefit, ExemptionReason, Brand, Category
from product.forms import ProductForm, NCMForm, CFOPForm, TaxBenefitForm, ExemptionReasonForm, BrandForm, CategoryForm

# Create your views here.
def product_list(request):
    create_form_data = request.session.get('create_form_data', None)
    #last_code = Product.objects.latest('id')
    products = Product.objects.order_by('-id')
    last_code = products.first().code if products.exists() else None  # Pega o primeiro produto ou None se não existir
    
    if last_code:  # Verifica se last_code não é None ou uma string vazia
        try:
            next_code = int(last_code) + 1  # Converte o last_code em inteiro e soma 1
        except ValueError:
            next_code = 1  # Define um valor padrão se a conversão falhar
    else:
        next_code = 1  # Define um valor padrão se não houver produto
        
    form = ProductForm(create_form_data, initial={
        'code': next_code
    })
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # Exibe 10 produtos por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os produtos
    context = {
        'form': form,
        'page_obj': page_obj
    }
    return render(request, 'product/product_list.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Adicionando request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com Sucesso!')
            return redirect('product:list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

# Validar Cadastro produto
def product_valid_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    FILES = request.FILES  # Capturar arquivos enviados
    request.session['create_form_data'] = POST
    form = ProductForm(POST, FILES)  # Passar arquivos para o formulário
    if form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado com Sucesso!')
        #fazemos a limpeza da sessão de criação do formulario
        del(request.session['create_form_data'])
    return redirect('product:list')


# Atualizar produto
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Adicionando request.FILES
        if form.is_valid():
            form.save()
            return redirect('product:list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

# Deletar produto
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Product:list')
    return render(request, 'product/product_confirm_delete.html', {'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})


# Views para NCM
def ncm_list(request):
    ncms = NCM.objects.all()
    paginator = Paginator(ncms, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/ncm_list.html', context)


def ncm_create(request):
    if request.method == 'POST':
        form = NCMForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'NCM cadastrado com sucesso!')
            return redirect('product:ncm_list')
    else:
        form = NCMForm()
    return render(request, 'product/ncm_form.html', {'form': form})


def ncm_update(request, pk):
    ncm = get_object_or_404(NCM, pk=pk)
    if request.method == 'POST':
        form = NCMForm(request.POST, instance=ncm)
        if form.is_valid():
            form.save()
            messages.success(request, 'NCM atualizado com sucesso!')
            return redirect('product:ncm_list')
    else:
        form = NCMForm(instance=ncm)
    return render(request, 'product/ncm_form.html', {'form': form})


def ncm_delete(request, pk):
    ncm = get_object_or_404(NCM, pk=pk)
    if request.method == 'POST':
        ncm.delete()
        messages.success(request, 'NCM excluído com sucesso!')
        return redirect('product:ncm_list')
    return render(request, 'product/ncm_confirm_delete.html', {'ncm': ncm})


# Views para CFOP
def cfop_list(request):
    cfops = CFOP.objects.all()
    paginator = Paginator(cfops, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/cfop_list.html', context)


def cfop_create(request):
    if request.method == 'POST':
        form = CFOPForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'CFOP cadastrado com sucesso!')
            return redirect('product:cfop_list')
    else:
        form = CFOPForm()
    return render(request, 'product/cfop_form.html', {'form': form})


def cfop_update(request, pk):
    cfop = get_object_or_404(CFOP, pk=pk)
    if request.method == 'POST':
        form = CFOPForm(request.POST, instance=cfop)
        if form.is_valid():
            form.save()
            messages.success(request, 'CFOP atualizado com sucesso!')
            return redirect('product:cfop_list')
    else:
        form = CFOPForm(instance=cfop)
    return render(request, 'product/cfop_form.html', {'form': form})


def cfop_delete(request, pk):
    cfop = get_object_or_404(CFOP, pk=pk)
    if request.method == 'POST':
        cfop.delete()
        messages.success(request, 'CFOP excluído com sucesso!')
        return redirect('product:cfop_list')
    return render(request, 'product/cfop_confirm_delete.html', {'cfop': cfop})


# Views para TaxBenefit
def taxbenefit_list(request):
    taxbenefits = TaxBenefit.objects.all()
    paginator = Paginator(taxbenefits, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/taxbenefit_list.html', context)


def taxbenefit_create(request):
    if request.method == 'POST':
        form = TaxBenefitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Benefício Fiscal cadastrado com sucesso!')
            return redirect('product:taxbenefit_list')
    else:
        form = TaxBenefitForm()
    return render(request, 'product/taxbenefit_form.html', {'form': form})


def taxbenefit_update(request, pk):
    taxbenefit = get_object_or_404(TaxBenefit, pk=pk)
    if request.method == 'POST':
        form = TaxBenefitForm(request.POST, instance=taxbenefit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Benefício Fiscal atualizado com sucesso!')
            return redirect('product:taxbenefit_list')
    else:
        form = TaxBenefitForm(instance=taxbenefit)
    return render(request, 'product/taxbenefit_form.html', {'form': form})


def taxbenefit_delete(request, pk):
    taxbenefit = get_object_or_404(TaxBenefit, pk=pk)
    if request.method == 'POST':
        taxbenefit.delete()
        messages.success(request, 'Benefício Fiscal excluído com sucesso!')
        return redirect('product:taxbenefit_list')
    return render(request, 'product/taxbenefit_confirm_delete.html', {'taxbenefit': taxbenefit})


# Views para ExemptionReason
def exemptionreason_list(request):
    exemptionreasons = ExemptionReason.objects.all()
    paginator = Paginator(exemptionreasons, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/exemptionreason_list.html', context)


def exemptionreason_create(request):
    if request.method == 'POST':
        form = ExemptionReasonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motivo de Desoneração cadastrado com sucesso!')
            return redirect('product:exemptionreason_list')
    else:
        form = ExemptionReasonForm()
    return render(request, 'product/exemptionreason_form.html', {'form': form})


def exemptionreason_update(request, pk):
    exemptionreason = get_object_or_404(ExemptionReason, pk=pk)
    if request.method == 'POST':
        form = ExemptionReasonForm(request.POST, instance=exemptionreason)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motivo de Desoneração atualizado com sucesso!')
            return redirect('product:exemptionreason_list')
    else:
        form = ExemptionReasonForm(instance=exemptionreason)
    return render(request, 'product/exemptionreason_form.html', {'form': form})


def exemptionreason_delete(request, pk):
    exemptionreason = get_object_or_404(ExemptionReason, pk=pk)
    if request.method == 'POST':
        exemptionreason.delete()
        messages.success(request, 'Motivo de Desoneração excluído com sucesso!')
        return redirect('product:exemptionreason_list')
    return render(request, 'product/exemptionreason_confirm_delete.html', {'exemptionreason': exemptionreason})


# Views para Brand
def brand_list(request):
    brands = Brand.objects.all()
    paginator = Paginator(brands, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/brand_list.html', context)


def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca cadastrada com sucesso!')
            return redirect('product:brand_list')
    else:
        form = BrandForm()
    return render(request, 'product/brand_form.html', {'form': form})


def brand_update(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca atualizada com sucesso!')
            return redirect('product:brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'product/brand_form.html', {'form': form})


def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Marca excluída com sucesso!')
        return redirect('product:brand_list')
    return render(request, 'product/brand_confirm_delete.html', {'brand': brand})


# Views para Category
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Pagina os itens
    context = {
        'page_obj': page_obj
    }
    return render(request, 'product/category_list.html', context)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('product:category_list')
    else:
        form = CategoryForm()
    return render(request, 'product/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('product:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product/category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('product:category_list')
    return render(request, 'product/category_confirm_delete.html', {'category': category})