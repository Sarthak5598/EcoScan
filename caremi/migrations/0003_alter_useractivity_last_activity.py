# Generated by Django 5.1.3 on 2024-11-19 09:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("caremi", "0002_alter_useractivity_last_activity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useractivity",
            name="last_activity",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
