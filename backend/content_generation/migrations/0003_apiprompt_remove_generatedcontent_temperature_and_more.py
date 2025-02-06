# Generated by Django 5.1.4 on 2025-02-05 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_generation', '0002_alter_generatedcontent_temperature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.TextField()),
                ('temperature', models.FloatField(default=0.7)),
                ('token_limit', models.IntegerField(default=256)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='generatedcontent',
            name='temperature',
        ),
        migrations.RemoveField(
            model_name='generatedcontent',
            name='token_limit',
        ),
        migrations.AlterField(
            model_name='generatedcontent',
            name='prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generated_contents', to='content_generation.apiprompt'),
        ),
    ]
