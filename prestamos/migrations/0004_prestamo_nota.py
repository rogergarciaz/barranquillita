# Generated by Django 3.0.8 on 2020-09-03 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0003_auto_20200728_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='nota',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]