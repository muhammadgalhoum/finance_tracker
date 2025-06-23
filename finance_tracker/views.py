import csv
from datetime import datetime
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import TransactionForm
from .models import Transaction, Category, MonthlySummary


@login_required
def transaction_list(request, category_id=None):
    user = request.user
    transactions = Transaction.objects.filter(user=user).select_related("category")
    selected_category = None
    empty_message = None

    # Filter by category
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        transactions = transactions.filter(category=selected_category)

    # Filter by selected date
    date_str = request.GET.get("date")
    if date_str:
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            transactions = transactions.filter(date=parsed_date)
        except ValueError:
            empty_message = "Invalid date format."

    if not transactions.exists():
        if selected_category and date_str:
            empty_message = "There are no transactions in this category on the selected date."
        elif selected_category:
            empty_message = "There are no transactions in this category."
        elif date_str:
            empty_message = "There are no transactions in the selected date."
        else:
            empty_message = "There are no transactions yet."

    categories = Category.objects.filter(transactions__user=user).distinct()

    context = {
        "transactions": transactions.order_by("-date"),
        "categories": categories,
        "selected_category": selected_category,
        "selected_date": date_str,
        "empty_message": empty_message,
    }
    return render(request, "finance_tracker/transaction_list.html", context)


@login_required
def transaction_search(request):
    user = request.user
    query = request.GET.get("q", "").strip()
    transactions = Transaction.objects.filter(
        user=user).select_related("category")
    message = None

    if query:
        transactions = transactions.filter(
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(amount__icontains=query)
        )

    if not transactions.exists():
        message = "There are no transactions matched with the search term."

    return render(request, "finance_tracker/transaction_search_results.html", {
        "transactions": transactions.order_by("-date"),
        "search_query": query,
        "message": message,
    })


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finance_tracker/transaction_form.html"
    success_url = reverse_lazy("finance_tracker:transaction_list")

    def form_valid(self, form):
        print("PK is:", form.instance.pk)
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finance_tracker/transaction_form.html"
    success_url = reverse_lazy("finance_tracker:transaction_list")
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "finance_tracker/transaction_confirm_delete.html"
    success_url = reverse_lazy("finance_tracker:transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


@login_required
def export_transactions_csv(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    # Filters
    date_str = request.GET.get("date")
    category_id = request.GET.get("category")
    query = request.GET.get("q", "").strip()

    if date_str:
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            transactions = transactions.filter(date=parsed_date)
        except ValueError:
            pass

    if category_id:
        transactions = transactions.filter(category_id=category_id)

    if query:
        transactions = transactions.filter(
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(amount__icontains=query)
        )

    # CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transactions.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Type', 'Amount', 'Description'])

    for t in transactions:
        writer.writerow(
            [t.date, t.category.name, t.category.type, t.amount, t.description])

    return response


@login_required
def monthly_summary_list(request):
    summaries = MonthlySummary.objects.filter(user=request.user)
    return render(request, "finance_tracker/monthly_summary_list.html", {"summaries": summaries})
