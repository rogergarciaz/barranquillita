# Generated by Django 3.0.8 on 2020-07-29 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salarios', '0003_produccion_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='fijo',
            name='area',
            field=models.CharField(default=None, max_length=20),
        ),
    ]