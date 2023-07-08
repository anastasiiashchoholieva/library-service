# tasks.py

from datetime import date
from celery import shared_task

from helpers.telegram_helper import send_telegram_message
from .models import Borrowing


@shared_task
def check_overdue_borrowings():
    today = date.today()
    overdue_borrowings = Borrowing.objects.filter(expected_return_date__lte=today, actual_return_date=None)

    if overdue_borrowings.exists():
        message = "Overdue borrowings:\n"
        for borrowing in overdue_borrowings:
            message += f"Book: {borrowing.book.title}, User: {borrowing.user.username}\n"

        send_telegram_message(message)
    else:
        send_telegram_message("No borrowings overdue today!")
