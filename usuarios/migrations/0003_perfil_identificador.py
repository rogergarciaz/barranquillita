# Generated by Django 3.0.8 on 2020-10-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_perfil_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='identificador',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
