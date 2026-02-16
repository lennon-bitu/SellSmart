# Generated manually to recreate the missing transaction_type_id foreign key
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('financial_control', '0001_initial'),
    ]

    operations = [
        # Adicionando o campo transaction_type_id como ForeignKey
        # O Django automaticamente adiciona o sufixo _id às chaves estrangeiras
        migrations.AddField(
            model_name='financialtransaction',
            name='transaction_type',
            field=models.ForeignKey(to='financial_control.TransactionType', on_delete=django.db.models.deletion.PROTECT, verbose_name='Tipo de Transação'),
        ),
    ]