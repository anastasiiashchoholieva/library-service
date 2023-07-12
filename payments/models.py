from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from borrowings.models import Borrowing


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        CANCELLED = "CANCELLED", _("Cancelled")

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", _("Payment")
        FINE = "FINE", _("Fine")

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT
    )
    borrowing_id = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    session_url = models.URLField(max_length=2000)
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse("payment-detail", args=[str(self.id)])

    def __str__(self):
        return f"Payment ID: {self.id}"
