# Generated by Django 4.2.1 on 2023-07-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PAYMENT", "Payment"), ("FINE", "Fine")],
                        default="PAYMENT",
                        max_length=20,
                    ),
                ),
                ("borrowing_id", models.IntegerField()),
                ("session_url", models.URLField()),
                ("session_id", models.CharField(max_length=100)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
