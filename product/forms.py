from django import forms
from .models import Product, CFOP, NCM, Brand, Category, TaxBenefit, ExemptionReason
from django.core.exceptions import ValidationError

'''
a função add_attr recebera o field, o nome do atributo que sera adicionado e seu valor
após isso pegamos o atributo existente e passando uma string vazia caso ele não exista
depois buscamos o atributo e setamos seu novo valor
'''
def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name,'')
    field.widget.attrs['attr_name'] = f'{existing_attr} {attr_new_val}'.strip()


'''
a função adiciona o placeholder aos fields ela recebe o field e o valor para o placeholder
'''
def add_placeholder(field, placeholder_val):
    add_attr(field,'placeholder',  placeholder_val)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code','name','category', 'brand', 'cost_price', 'price', 'stock', 'is_active', 'image']
        labels = {
            'name':'Nome'
        }
        '''
        no help_texts, colocamos os texto de ajuda que fica a baixo de nossas fields
        '''
        help_texts = {
            'name':'digite um nome para o produto',
            'category': 'Informe a Categoria',
            'brand': 'Informe a marca do produto',
        }
        '''
        nas error_messages, definimos as mensagem de erro de acordo com as validações de nossas fields
        como por exemplo o required, invalid para uma mensagem mais generica
        '''
        error_messages = {
            'name': {'required':'Este campo e Obrigatório'},
            'price': {'required':'Este campo e Obrigatório', 'invalid':'Valor invalido'},
        }
        '''
        no widgets adicionamos os atributos para os fields do formulario como por exemplo o placeholder, class, type e outros
        '''
        # widgets = {
        #     'code': forms.NumberInput(attrs={
        #         'disabled':'False'
        #     }),
        # }

    '''
    validação de dados do campo e fazendo lançamento de erros
    '''
    def clean_price(self):
        data = self.cleaned_data.get('price')
        if data <= 0:
            raise ValidationError('O valor tem que ser maior que *0*', code='invalid')
        return data
    

    def clean_email(self):
        code = self.cleaned_data.get('code','')
        exists = Product.objects.filter(code=code).exists
        if exists:
            raise ValidationError('Esse código ja existe cadastrado', code='invalid')
        return code
    

    def __init__(self, *args, **kwargs): # Adiciona class CSS nos fields
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        #exeplo do uso da função add_placeholder
        #add_placeholder(self.fields['name'], 'Produto')


class NCMForm(forms.ModelForm):
    class Meta:
        model = NCM
        fields = ['code', 'name', 'description', 'type', 'is_active']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'is_active': 'Ativo'
        }
        help_texts = {
            'code': 'Digite o código da NCM',
            'name': 'Digite o nome da NCM',
            'description': 'Forneça uma descrição detalhada',
            'type': 'Selecione o tipo de NCM',
            'is_active': 'Marque se a NCM estiver ativa'
        }
        error_messages = {
            'code': {
                'required': 'Este campo é obrigatório',
                'unique': 'Já existe uma NCM com este código'
            },
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class CFOPForm(forms.ModelForm):
    class Meta:
        model = CFOP
        fields = ['code', 'name', 'description', 'type', 'is_active']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'is_active': 'Ativo'
        }
        help_texts = {
            'code': 'Digite o código do CFOP',
            'name': 'Digite o nome do CFOP',
            'description': 'Forneça uma descrição detalhada',
            'type': 'Selecione o tipo de CFOP',
            'is_active': 'Marque se o CFOP estiver ativo'
        }
        error_messages = {
            'code': {
                'required': 'Este campo é obrigatório',
                'unique': 'Já existe um CFOP com este código'
            },
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class TaxBenefitForm(forms.ModelForm):
    class Meta:
        model = TaxBenefit
        fields = ['code', 'name', 'description', 'type', 'is_active']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'is_active': 'Ativo'
        }
        help_texts = {
            'code': 'Digite o código do Benefício Fiscal',
            'name': 'Digite o nome do Benefício Fiscal',
            'description': 'Forneça uma descrição detalhada',
            'type': 'Selecione o tipo de Benefício Fiscal',
            'is_active': 'Marque se o Benefício Fiscal estiver ativo'
        }
        error_messages = {
            'code': {
                'required': 'Este campo é obrigatório',
                'unique': 'Já existe um Benefício Fiscal com este código'
            },
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class ExemptionReasonForm(forms.ModelForm):
    class Meta:
        model = ExemptionReason
        fields = ['code', 'name', 'description', 'type', 'is_active']
        labels = {
            'code': 'Código',
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'is_active': 'Ativo'
        }
        help_texts = {
            'code': 'Digite o código do Motivo de Desoneração',
            'name': 'Digite o nome do Motivo de Desoneração',
            'description': 'Forneça uma descrição detalhada',
            'type': 'Selecione o tipo de Motivo de Desoneração',
            'is_active': 'Marque se o Motivo de Desoneração estiver ativo'
        }
        error_messages = {
            'code': {
                'required': 'Este campo é obrigatório',
                'unique': 'Já existe um Motivo de Desoneração com este código'
            },
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'is_active']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'is_active': 'Ativo'
        }
        help_texts = {
            'name': 'Digite o nome da marca',
            'description': 'Forneça uma descrição detalhada',
            'is_active': 'Marque se a marca estiver ativa'
        }
        error_messages = {
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'is_active': 'Ativo'
        }
        help_texts = {
            'name': 'Digite o nome da categoria',
            'description': 'Forneça uma descrição detalhada',
            'is_active': 'Marque se a categoria estiver ativa'
        }
        error_messages = {
            'name': {
                'required': 'Este campo é obrigatório'
            }
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
