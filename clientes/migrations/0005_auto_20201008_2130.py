# Generated by Django 3.0.8 on 2020-10-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_cliente_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='identificador',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='compra',
            name='credito',
            field=models.BooleanField(default=False),
        ),
    ]
