# Generated by Django 5.0.7 on 2024-09-18 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SunApp', '0005_facture_lignefacture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lignefacture',
            name='facture',
        ),
        migrations.RemoveField(
            model_name='lignefacture',
            name='product',
        ),
        migrations.DeleteModel(
            name='Facture',
        ),
        migrations.DeleteModel(
            name='LigneFacture',
        ),
    ]
