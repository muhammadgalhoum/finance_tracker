import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator


class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    type = models.CharField(max_length=7, choices=Type.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("finance_tracker:transaction_list_by_category", args=[str(self.id)])

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        verbose_name = "Montly Summary"
        verbose_name_plural = "Monthly Summaries"

    def __str__(self):
        return f"{self.date} | {self.category.name} | {self.amount}"


class MonthlySummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ["user", "month"]
        ordering = ["-month"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"
