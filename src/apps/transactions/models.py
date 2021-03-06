from django.db import models
from ..accounts.models import Employee, Member
from ..items.models import Items


class PaymentMethod(models.Model):
    name = models.CharField(max_length=25)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'payment_methods'


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='transactions')
    card_number = models.IntegerField(null=True, blank=True)
    paid_of = models.BooleanField(default=False)
    customer_purchase = models.FloatField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.employee)

    class Meta:
        db_table = 'transactions'


class DetailTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='detail_transactions')
    detail_item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='detail_transactions')
    quantity = models.IntegerField(default=1)
    item_price = models.IntegerField(null=True, blank=True)
    sub_total = models.IntegerField(null=True, blank=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return str(self.quantity)

    class Meta:
        db_table = 'detail_transactions'
