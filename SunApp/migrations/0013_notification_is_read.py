# Generated by Django 5.0.7 on 2024-09-25 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SunApp', '0012_remove_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
