# Generated by Django 5.0.7 on 2024-10-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SunApp', '0014_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pays',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quartier',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='ville',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
