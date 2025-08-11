from django.db import models

class TradeOperations(models.Model):
    pk = models.CompositePrimaryKey(
        "trade_date", "operation", "market", "institution", "ticker", "quantity", "price"
    )
    trade_date = models.DateField()
    operation = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    due_date = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.trade_date} - {self.ticker} - {self.quantity}@{self.price}'
