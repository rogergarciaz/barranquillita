# Generated by Django 3.0.8 on 2020-07-21 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salarios', '0002_auto_20200721_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='produccion',
            name='nota',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
