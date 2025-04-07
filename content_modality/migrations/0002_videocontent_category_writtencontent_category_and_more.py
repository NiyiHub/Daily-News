# Generated by Django 5.1.4 on 2025-04-07 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_modality', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocontent',
            name='category',
            field=models.CharField(choices=[('US', 'U.S'), ('WORLD', 'World'), ('POLITICS', 'Politics'), ('HEALTH', 'Health'), ('SCI_TECH', 'Science & Tech'), ('BUSINESS', 'Business'), ('LIFESTYLE', 'Lifestyle'), ('OPINION', 'Opinion'), ('MEDIA', 'Media'), ('SPORTS', 'Sports'), ('WEATHER', 'Weather')], default='US', max_length=20),
        ),
        migrations.AddField(
            model_name='writtencontent',
            name='category',
            field=models.CharField(choices=[('US', 'U.S'), ('WORLD', 'World'), ('POLITICS', 'Politics'), ('HEALTH', 'Health'), ('SCI_TECH', 'Science & Tech'), ('BUSINESS', 'Business'), ('LIFESTYLE', 'Lifestyle'), ('OPINION', 'Opinion'), ('MEDIA', 'Media'), ('SPORTS', 'Sports'), ('WEATHER', 'Weather')], default='US', max_length=20),
        ),
        migrations.AddField(
            model_name='writtenimagecontent',
            name='category',
            field=models.CharField(choices=[('US', 'U.S'), ('WORLD', 'World'), ('POLITICS', 'Politics'), ('HEALTH', 'Health'), ('SCI_TECH', 'Science & Tech'), ('BUSINESS', 'Business'), ('LIFESTYLE', 'Lifestyle'), ('OPINION', 'Opinion'), ('MEDIA', 'Media'), ('SPORTS', 'Sports'), ('WEATHER', 'Weather')], default='US', max_length=20),
        ),
    ]
