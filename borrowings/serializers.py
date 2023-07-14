import asyncio
from rest_framework import serializers

from books.serializers import BookSerializer

from borrowings.models import Borrowing
from helpers.payment_helper import create_stripe_session
from helpers.telegram_helper import send_telegram_message
from payments.serializers import PaymentSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payments",
        ]

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user
        request = self.context["request"]

        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to borrow a book.")

        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        borrowing = Borrowing.objects.create(
            expected_return_date=validated_data["expected_return_date"],
            book=book,
            user=user
        )

        create_stripe_session(borrowing, request)

        book.inventory -= 1
        book.save()

        message = f"New borrowing created: Book {book.title}, User {user.id}: {user.email}. " \
                  f"The return is expected on {borrowing.expected_return_date}."

        asyncio.run(send_telegram_message(message))

        return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payments"
        ]


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payments"
        ]


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "book", "user"]
        read_only_fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        ]
