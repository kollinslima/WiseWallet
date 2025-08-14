from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

UNKNOWN_CLASSIFICATION = "UNKNOWN"
UNKNOWN_TICKER         = "UNKNOWN"
UNKNOWN_INSTITUTION    = "UNKNOWN"

class AssetClassificationManager(models.Manager):
    def get_classifications(self, user):
        return super().get_queryset().filter(user=user)

class AssetClassification(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'type'], name='unique_asset_classification')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, default=UNKNOWN_CLASSIFICATION)

    objects = models.Manager()
    user_classifications = AssetClassificationManager()

class AssetIdentificationManager(models.Manager):
    def get_identification(self, user):
        return super().get_queryset().filter(user=user)

class AssetIdentification(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'ticker'], name='unique_asset_identification')
        ]

    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker         = models.CharField(max_length=10, default=UNKNOWN_TICKER)
    name           = models.CharField(max_length=100, blank=True)
    classification = models.ForeignKey(AssetClassification,
                                             on_delete=models.SET_DEFAULT,
                                             default=UNKNOWN_CLASSIFICATION)

    objects = models.Manager()
    user_asset_identification = AssetIdentificationManager()

class TransactionInstitutionsManager(models.Manager):
    def get_institutions(self, user):
        return super().get_queryset().filter(user=user)

class TransactionInstitutions(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_transaction_institution')
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=UNKNOWN_INSTITUTION)

    objects = models.Manager()
    user_institutions = TransactionInstitutionsManager()

class TransactionOperationsManager(models.Manager):
    def get_operations(self, user):
        return super().get_queryset().filter(user=user)

class TransactionOperations(models.Model):

    class TransactionOperation(models.TextChoices):
        BUY               = "Buy", _("Buy")
        SELL              = "Sell", _("Sell")
        UNKNOWN_OPERATION = "Unknown", _("UNKNOWN_OPERATION")

    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    asset            = models.ForeignKey(AssetIdentification,
                                         on_delete=models.CASCADE)
    institution_name = models.ForeignKey(TransactionInstitutions,
                                         on_delete=models.SET_DEFAULT,
                                         default=UNKNOWN_INSTITUTION)
    operation        = models.CharField(choices=TransactionOperation)
    operation_date   = models.DateField(null=True, blank=True)
    settlement_date  = models.DateField()
    amount           = models.DecimalField(max_digits=30, decimal_places=18)
    total_value      = models.DecimalField(max_digits=12, decimal_places=2)
    fees             = models.DecimalField(max_digits=12,
                                           decimal_places=2,
                                           default=0)

    objects = models.Manager()
    user_operations = TransactionOperationsManager()

