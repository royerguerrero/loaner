# Generated by Django 5.0.6 on 2024-06-05 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loans", "0003_alter_loan_contract_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="taken_at",
            field=models.DateTimeField(null=True),
        ),
    ]
