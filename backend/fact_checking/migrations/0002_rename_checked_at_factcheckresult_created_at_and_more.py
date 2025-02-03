# Generated by Django 5.1.4 on 2025-02-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_checking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factcheckresult',
            old_name='checked_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='factcheckresult',
            name='evidence',
        ),
        migrations.RemoveField(
            model_name='factcheckresult',
            name='status',
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='accuracy_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='clarity_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='composite_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='details',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='disclosure_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='factcheckresult',
            name='source_score',
            field=models.FloatField(default=0.0),
        ),
    ]
