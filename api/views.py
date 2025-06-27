import csv
from django.http import HttpResponse
from rest_framework import generics, viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    UserRegistrationSerializer, 
    TransactionSerializer,
    CategorySerializer,
    MonthlySummarySerializer,
)

from finance_tracker.models import Transaction, Category, MonthlySummary


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["description", "amount", "category__name"]
    ordering_fields = ["date", "amount"]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class MonthlySummaryListView(generics.ListAPIView):
    serializer_class = MonthlySummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MonthlySummary.objects.filter(user=self.request.user)


class MonthlySummaryDetailView(generics.RetrieveAPIView):
    serializer_class = MonthlySummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MonthlySummary.objects.filter(user=self.request.user)


class TransactionExportCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"

        writer = csv.writer(response)
        writer.writerow(["Date", "Amount", "Category", "Type", "Description"])

        for t in transactions:
            writer.writerow([t.date, t.amount, t.category.name, t.category.type, t.description])

        return response
