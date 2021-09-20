from django.contrib import admin
from .models import PaymentMethod, Transaction, DetailTransaction


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "create_at", "update_at")


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ("member", "sales", "payment_method", "card_number", "customer_purchase","paid_of", "create_at", "update_at")


class DetailTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction", "detail_item", "quantity", "create_at", "update_at")


admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Transaction, TransactionsAdmin)
admin.site.register(DetailTransaction, DetailTransactionAdmin)
