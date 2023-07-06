from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        if user.is_authenticated:
            return Borrowing.objects.filter(user=user)
        return Borrowing.objects.none()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
