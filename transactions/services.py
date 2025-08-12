import logging
import openpyxl
import pandas as pd
import pandas_market_calendars as mcal

from .models import AssetClassification, AssetIdentification
from .models import TransactionInstitutions, TransactionOperations
from .models import UNKNOWN_CLASSIFICATION
from datetime import date, datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from enum import StrEnum

class B3TransactionsReportHeader(StrEnum):
    IN_OUT_TRANSACTION_TYPE = "Entrada/Saída"
    DATE                    = "Data"
    TRANSACTION_TYPE        = "Movimentação"
    ASSET_DESCRIPTION       = "Produto"
    INSTITUTION             = "Instituição"
    AMOUNT                  = "Quantidade"
    TRANSACTION_VALUE       = "Valor da Operação"

# Money out of my account is expressed as "Credito"
# Money into my account is expressed as "Debito"
class B3InOutTransactionTypes(StrEnum):
    OUT = "Credito"
    IN  = "Debito"

class B3TransactionTypes(StrEnum):
    TRADE_SETTLEMENT = "Transferência - Liquidação"


def _get_transaction_operation(settlement_date):
    b3_calendar = mcal.get_calendar('B3')

    b3_business_day = pd.tseries.offsets.CustomBusinessDay(
        calendar=b3_calendar.holidays().holidays
    )

    data_liquidacao_ts = pd.to_datetime(settlement_date)

    # Settlement is D+2 for B3
    data_operacao_ts = data_liquidacao_ts - (2 * b3_business_day)

    return data_operacao_ts.date()

def _get_transaction_operation(in_out_operation, transaction_type):
    transaction_operation = TransactionOperations.TransactionOperation.UNKNOWN_OPERATION

    if transaction_type == B3TransactionTypes.TRADE_SETTLEMENT:
        if in_out_operation == B3InOutTransactionTypes.OUT:
            transaction_operation = TransactionOperations.TransactionOperation.BUY
        elif in_out_operation == B3InOutTransactionTypes.IN:
            transaction_operation = TransactionOperations.TransactionOperation.SELL

    return transaction_operation


def process_transactions_file(file):
    if not file.name.endswith('.xlsx'):
        raise ValidationError("Invalid file format. Please upload a .xlsx file.")
    try:
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        
        # Get header row
        header = [cell.value for cell in sheet[1]]
        
    except Exception as e:
        raise ValidationError("Cannot open XLSX file.")
    
    try:
        with transaction.atomic():
            for row_index in range(2, sheet.max_row + 1):
                row_values = [cell.value for cell in sheet[row_index]]
                row_entry = dict(zip(header, row_values))

                transaction_operation = _get_transaction_operation(
                    row_entry[B3TransactionsReportHeader.IN_OUT_TRANSACTION_TYPE],
                    row_entry[B3TransactionsReportHeader.TRANSACTION_TYPE]
                )

                if transaction_operation == TransactionOperations.TransactionOperation.UNKNOWN_OPERATION:
                    continue

                asset_description = row_entry[B3TransactionsReportHeader.ASSET_DESCRIPTION].split("-")

                asset_classification,_ = AssetClassification.objects.get_or_create(
                    asset_type = UNKNOWN_CLASSIFICATION
                )
                
                asset_identification,_ = AssetIdentification.objects.get_or_create(
                        asset_ticker         = asset_description[0],
                        asset_name           = asset_description[1],
                        asset_classification = asset_classification
                )

                institution = row_entry[B3TransactionsReportHeader.INSTITUTION]

                transaction_institution,_ = TransactionInstitutions.objects.get_or_create(
                        institution_name = institution
                )

                settlement_date = datetime.strptime(
                                    row_entry[B3TransactionsReportHeader.DATE],
                                    '%d/%m/%Y').date()

                amount = int(row_entry[B3TransactionsReportHeader.AMOUNT])

                transaction_value = (str(row_entry[B3TransactionsReportHeader.TRANSACTION_VALUE])
                                        .replace('R$', '')
                                        .strip()
                                        .replace('.', '')
                                        .replace(',', '.'))
                total_value = Decimal(transaction_value)

                TransactionOperations.objects.create(
                    asset=asset_identification,
                    institution_name=transaction_institution,
                    operation=transaction_operation,
                    settlement_date=settlement_date,
                    amount=amount,
                    total_value=total_value,
                )

    except (ValueError, KeyError, TypeError) as e:
        raise ValidationError(f"Invalid data in row: {row_entry}. Error: {e}")

