# Generated by Django 5.0.8 on 2024-09-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0014_brovides_services_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='brovides_services',
            name='debt_cleared_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
