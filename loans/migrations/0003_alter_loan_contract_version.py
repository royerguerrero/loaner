# Generated by Django 5.0.6 on 2024-06-05 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loans", "0002_alter_loan_outstanding_alter_loan_taken_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="contract_version",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
