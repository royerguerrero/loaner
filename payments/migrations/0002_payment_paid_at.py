# Generated by Django 5.0.6 on 2024-06-05 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="paid_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 6, 5, 13, 57, 28, 474, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
    ]
