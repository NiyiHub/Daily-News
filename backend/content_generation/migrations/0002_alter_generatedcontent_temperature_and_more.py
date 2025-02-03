# Generated by Django 5.1.4 on 2025-02-02 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_generation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedcontent',
            name='temperature',
            field=models.FloatField(default=0.7),
        ),
        migrations.AlterField(
            model_name='generatedcontent',
            name='token_limit',
            field=models.IntegerField(default=256),
        ),
    ]
