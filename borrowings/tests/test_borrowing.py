import datetime

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer

BORROWING_URL = reverse("borrowings:borrowing-list")


def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Test author",
        "cover": "HARD",
        "inventory": 2,
        "daily_fee": 0.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(**params):
    book = sample_book()
    defaults = {
        "book": book,
        "user": get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        ),
        "expected_return_date": "2023-07-15",
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required_post(self):
        res = self.client.post(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_get(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        sample_borrowing(user=self.user)

        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "book": book.id,
            "expected_return_date": "2023-07-15",
            "user": self.user.id,
        }

        res = self.client.post(BORROWING_URL, payload)
        borrowing = Borrowing.objects.get(id=res.data["id"])

        self.assertEqual(payload["book"], getattr(borrowing.book, "id"))
        self.assertEqual(
            payload["expected_return_date"],
            str(getattr(borrowing, "expected_return_date")),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_auth_required_get(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "book": book.id,
            "expected_return_date": "2023-07-15",
            "user": self.user.id,
        }

        res = self.client.post(BORROWING_URL, payload)
        borrowing = Borrowing.objects.get(id=res.data["id"])

        self.assertEqual(payload["book"], getattr(borrowing.book, "id"))
        self.assertEqual(
            payload["expected_return_date"],
            str(getattr(borrowing, "expected_return_date")),
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
