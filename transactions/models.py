from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import auto

UNKNOWN_CLASSIFICATION = "UNKNOWN"
UNKNOWN_INSTITUTION    = "UNKNOWN"

class AssetClassification(models.Model):
    asset_type = models.CharField(max_length=100, primary_key=True)

class AssetIdentification(models.Model):
    asset_ticker         = models.CharField(max_length=10, primary_key=True)
    asset_name           = models.CharField(max_length=100, blank=True)
    asset_classification = models.ForeignKey(AssetClassification,
                                             on_delete=models.SET_DEFAULT,
                                             default=UNKNOWN_CLASSIFICATION)

class TransactionInstitutions(models.Model):
    institution_name = models.CharField(max_length=100, primary_key=True)

class TransactionOperations(models.Model):

    class TransactionOperation(models.IntegerChoices):
        BUY               = auto(), _("Buy")
        SELL              = auto(), _("Sell")
        UNKNOWN_OPERATION = auto(), _("UNKNOWN_OPERATION")

    asset            = models.ForeignKey(AssetIdentification,
                                         on_delete=models.CASCADE)
    institution_name = models.ForeignKey(TransactionInstitutions,
                                         on_delete=models.SET_DEFAULT,
                                         default=UNKNOWN_INSTITUTION)
    operation        = models.IntegerField(choices=TransactionOperation)
    operation_date   = models.DateField(null=True, blank=True)
    settlement_date  = models.DateField()
    amount           = models.DecimalField(max_digits=30, decimal_places=18)
    total_value      = models.DecimalField(max_digits=12, decimal_places=2)
    fees             = models.DecimalField(max_digits=12,
                                           decimal_places=2,
                                           default=0)

