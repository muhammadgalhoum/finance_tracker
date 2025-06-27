from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    TransactionViewSet,
    CategoryListView,
    CategoryDetailView,
    MonthlySummaryListView,
    MonthlySummaryDetailView,
    TransactionExportCSV,
)


app_name = "api"


router = DefaultRouter()
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<uuid:pk>/",CategoryDetailView.as_view(), name="category-detail"),
    path("summaries/", MonthlySummaryListView.as_view(),
         name="monthly-summary-list"),
    path("summaries/<uuid:pk>/", MonthlySummaryDetailView.as_view(),
         name="monthly-summary-detail"),
    path("transactions/export/", TransactionExportCSV.as_view(),
         name="transaction-export-csv"),
]

urlpatterns += router.urls
