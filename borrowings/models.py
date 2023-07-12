from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_active(self) -> bool:
        return self.actual_return_date is None

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expected_return_date__gte=models.F("borrow_date")),
                name="expected_return_date_gte_borrow_date"
            ),
            models.CheckConstraint(
                check=(models.Q(actual_return_date__isnull=True)
                       | models.Q(actual_return_date__gte=models.F("borrow_date"))),
                name="actual_return_date_gte_borrow_date_or_null"
            ),
        ]
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"Book {self.book.id} was borrowed by user {self.user.id} on {self.borrow_date}. " \
               f"It is expected to be returned by {self.expected_return_date}"
