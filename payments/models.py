from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = 'PAID', _('Paid')

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
    borrowing_id = models.IntegerField()
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse("payment-detail", args=[str(self.id)])

    def __str__(self):
        return f"Payment ID: {self.id}"