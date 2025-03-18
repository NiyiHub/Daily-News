# Generated by Django 5.1.4 on 2025-03-18 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FactCheckResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim', models.TextField()),
                ('verification_score', models.FloatField(default=0.0)),
                ('textual_rating', models.CharField(blank=True, max_length=50)),
                ('evidence', models.JSONField(blank=True, default=dict, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
