from django import forms
from .models import Product
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
        fields = ['name','category', 'brand', 'cost_price', 'price', 'stock', 'is_active', 'image']
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
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder':'Produto'
            }),
        }

    '''
    validação de dados do campo e fazendo lançamento de erros
    '''
    def clean_price(self):
        data = self.cleaned_data.get('price')
        if data <= 0:
            raise ValidationError('O valor tem que ser maior que *0*', code='invalid')
        return data
    
    def __init__(self, *args, **kwargs): # Adiciona class CSS nos fields
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'
        #exeplo do uso da função add_placeholder
        add_placeholder(self.fields['name'], 'Produto')
