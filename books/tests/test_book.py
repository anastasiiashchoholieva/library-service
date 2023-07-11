from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")


def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Test author",
        "cover": "Hardcover",
        "inventory": 2,
        "daily_fee": 0.99,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_post(self):
        res = self.client.post(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_get(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test pass",
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required_post(self):
        res = self.client.post(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_get(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "Sample book",
            "author": "Test author",
            "cover": "HARD",
            "inventory": 2,
            "daily_fee": 0.99,
        }

        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=res.data["id"])
        serializer = BookSerializer(book)
        self.assertEqual(res.data, serializer.data)
