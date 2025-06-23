from django.urls import path

from .views import (
    transaction_list,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    transaction_search,
    export_transactions_csv,
    monthly_summary_list,
)

app_name = "finance_tracker"

urlpatterns = [
    path("", transaction_list, name="transaction_list"),
    path("categories/<uuid:category_id>/", transaction_list,
         name="transaction_list_by_category"),
    path("search/", transaction_search, name="transaction_search"),
    path("create/", TransactionCreateView.as_view(),
         name="transaction_create"),
    path("update/<uuid:pk>/", TransactionUpdateView.as_view(),
         name="transaction_update"),
    path("delete/<uuid:pk>/", TransactionDeleteView.as_view(),
         name="transaction_delete"),
    path("export/csv/", export_transactions_csv,
         name="export_transactions_csv"),
    path("summaries/", monthly_summary_list, name="monthly_summary_list"),
]
