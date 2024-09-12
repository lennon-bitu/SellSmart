from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import forms

class RegisterForm(ModelForm):
    class Meta:
        model =  User
        #fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'