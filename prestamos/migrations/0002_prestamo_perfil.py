# Generated by Django 3.0.8 on 2020-07-21 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_perfil_area'),
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='perfil',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil'),
        ),
    ]