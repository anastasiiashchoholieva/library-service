# Generated by Django 4.2.1 on 2023-07-11 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("borrowings", "0001_initial"),
        ("payments", "0002_alter_payment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="borrowing_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="borrowings.borrowing",
            ),
        ),
    ]
