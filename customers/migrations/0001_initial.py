# Generated by Django 5.0.6 on 2024-06-04 00:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Active"), (2, "Inactive")], default=1
                    ),
                ),
                ("preaprroved_at", models.DateTimeField()),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
