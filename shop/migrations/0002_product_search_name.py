# Generated by Django 5.1.3 on 2025-02-07 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
