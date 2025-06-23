from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Transaction, MonthlySummary


@shared_task
def generate_monthly_summaries():
    today = timezone.localdate()
    month_start = today.replace(day=1)

    User = get_user_model()
    for user in User.objects.all():
        user_transactions = Transaction.objects.filter(
            user=user,
            date__year=month_start.year,
            date__month=month_start.month
        )

        income = sum(t.amount for t in user_transactions if t.category.type == "income")
        expenses = sum(t.amount for t in user_transactions if t.category.type == "expense")
        balance = income - expenses


        MonthlySummary.objects.update_or_create(
            user=user,
            month=month_start,
            defaults={
                "income": income,
                "expenses": abs(expenses),
                "balance": balance
            }
        )
    return f"Monthly summaries generated for {month_start.strftime('%B %Y')}"
