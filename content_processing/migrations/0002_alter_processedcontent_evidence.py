# Generated by Django 5.1.4 on 2025-03-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processedcontent',
            name='evidence',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
