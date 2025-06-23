import csv
from django.contrib import admin
from django.http import HttpResponse

from .models import Transaction, Category, MonthlySummary


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'category', 'date', 'description']
    list_filter = ['category', 'date']
    search_fields = ['description']
    ordering = ['date']
    actions = ['export_as_csv']
    
    @admin.action(description="Export selected transactions as CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=transactions.csv'
        writer = csv.writer(response)

        # Write header
        writer.writerow(['User', 'Category', 'Type', 'Amount', 'Date', 'Description'])

        # Write data rows
        for transaction in queryset:
            writer.writerow([
                transaction.user.username,
                transaction.category.name,
                transaction.category.type,
                transaction.amount,
                transaction.date,
                transaction.description
            ])

        return response


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    list_editable = ['type']
    search_fields = ['name']


@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'income', 'expenses', 'balance']
    list_filter = ['month']
