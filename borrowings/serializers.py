from rest_framework import serializers

import books

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active"
        ]

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user

        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to borrow a book.")

        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        borrowing = Borrowing.objects.create(
            expected_return_date=validated_data["expected_return_date"],
            actual_return_date=validated_data["actual_return_date"],
            book=book,
            user=user
        )

        book.inventory -= 1
        book.save()

        return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active"
        ]


class BorrowingDetailSerializer(BorrowingSerializer):
    book = books.serializers.BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active"
        ]


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "book", "user"]
        read_only_fields = ["borrow_date", "expected_return_date", "actual_return_date", "book", "user"]
