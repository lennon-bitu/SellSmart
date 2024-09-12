from django.db import models

# Modelo para NCM (Nomenclatura Comum do Mercosul)
class NCM(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')  # Código único para NCM
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome da NCM
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')  # Descrição da NCM
    type = models.CharField(max_length=50, verbose_name='Tipo')  # Tipo de NCM
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['code']
        verbose_name = 'NCM'
        verbose_name_plural = 'NCM'

    def __str__(self):
        return self.code

# Modelo para CFOP (Código Fiscal de Operações e Prestações)
class CFOP(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')  # Código único para CFOP
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome da CFOP
    description = models.TextField(blank=True, null=True, verbose_name='Descição')  # Descrição da CFOP
    type = models.CharField(max_length=50, verbose_name='Tipo')  # Tipo de CFOP
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['code']
        verbose_name = 'CFOP'
        verbose_name_plural = 'CFOPs'

    def __str__(self):
        return self.code

# Modelo para Benefício Fiscal
class TaxBenefit(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')  # Código único para o benefício fiscal
    name = models.CharField(max_length=255, verbose_name='nome')  # Nome do benefício fiscal
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')  # Descrição do benefício fiscal
    type = models.CharField(max_length=50, verbose_name='Tipo')  # Tipo do benefício fiscal
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['code']
        verbose_name = 'Beneficio Fiscal'
        verbose_name_plural = 'Beneficio Fiscal'

    def __str__(self):
        return self.name

# Modelo para Motivo de Desoneração
class ExemptionReason(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='código')  # Código único para o motivo de desoneração
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome do motivo de desoneração
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')  # Descrição do motivo de desoneração
    type = models.CharField(max_length=50, verbose_name='Tipo')  # Tipo do motivo de desoneração
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Motivo de Desoneração'
        verbose_name_plural = 'Motivo de Desoneração'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome do motivo de desoneração
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')  # Descrição do motivo de desoneração
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome do motivo de desoneração
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')  # Descrição do motivo de desoneração
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

# Modelo para Produto
class Product(models.Model):
    PRODUCT_TAX_CHOICES = [
        ('T', 'Tributado'),  # Produto tributado
        ('I', 'Isento'),  # Produto isento
        ('N', 'Não tributado'),  # Produto não tributado
        ('F', 'Substituição Tributária')  # Substituição tributária
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name='Código')  # Código do produto
    name = models.CharField(max_length=255, verbose_name='Nome')  # Nome do produto
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, verbose_name='Preço de custo')  # Preço de custo (opcional)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')  # Preço de venda
    stock = models.IntegerField(null=True, blank=True, verbose_name='Estoque')  # Quantidade em estoque (opcional)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0, verbose_name='Margem de Lucro')
    profit_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, default=0.0, verbose_name='Lucro')
    taxation = models.CharField(max_length=20, choices=PRODUCT_TAX_CHOICES ,null=True, blank=True, verbose_name='Tributação')  # Tributação do produto (opcional)
    ncm = models.ForeignKey(NCM,null=True, blank=True, on_delete=models.CASCADE)  # Chave estrangeira para NCM (opcional)
    cfop = models.ForeignKey(CFOP,null=True, blank=True, on_delete=models.CASCADE)  # Chave estrangeira para CFOP (opcional)
    icms_rate = models.DecimalField(max_digits=5, decimal_places=2 ,null=True, blank=True, verbose_name='% ICMS')  # Alíquota de ICMS (opcional)
    ipi = models.DecimalField(max_digits=5, decimal_places=2 ,null=True, blank=True, verbose_name='% IPI')  # Alíquota de IPI (opcional)
    cst_ipi = models.CharField(max_length=3 ,null=True, blank=True, verbose_name='Código cst IPI')  # Código CST para IPI (opcional)
    pis = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name='% PIS')  # Alíquota de PIS (opcional)
    cofins = models.DecimalField(max_digits=5, decimal_places=2 ,null=True, blank=True, verbose_name='% Cofins')  # Alíquota de COFINS (opcional)
    cst_pis = models.CharField(max_length=3, null=True, blank=True, verbose_name='Código cst PIS' )  # Código CST para PIS (opcional)
    cst_cofins = models.CharField(max_length=3, null=True, blank=True, verbose_name='Código cst Cofins')  # Código CST para COFINS (opcional)
    tax_benefit = models.ForeignKey(TaxBenefit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Beneficio fiscal')  # Benefício fiscal (opcional)
    exemption_reason = models.ForeignKey(ExemptionReason, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Motivo de desoneração')  # Motivo de desoneração (opcional)
    fcp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Fundo de combate a pobreza')  # Fundo de Combate à Pobreza (opcional)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Marca')  # Chave estrangeira para NCM  # Marca do produto (opcional)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True,  verbose_name='Categoria')  # Chave estrangeira para NCM  # Categoria do produto (opcional)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    image = models.ImageField("Image", upload_to="images/produto", blank=True, default="")

    class Meta:
        ordering = ['code']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produto'

    def __str__(self):
        return self.name
