import csv
import io

from .models import TradeOperation
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction

def process_transactions_file(file):
    try:
        if file.content_type != 'text/csv':
            raise

        reader = csv.DictReader(io.TextIOWrapper(file, encoding='utf-8'))
    except Exception as e:
        raise ValidationError("Cannot open CSV file.")
    
    with transaction.atomic():
        for row in reader:
            try:
                trade_date = datetime.strptime(row["Data do Negócio"], '%d/%m/%Y').date()
                operation = row["Tipo de Movimentação"]
                market = row["Mercado"]
                due_date_str = row["Prazo/Vencimento"]
                due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date() if due_date_str != '-' else None
                institution = row["Instituição"]
                ticker = row["Código de Negociação"]
                quantity = int(row["Quantidade"])
                price_str = row["Preço"].replace('R$', '').strip().replace('.', '').replace(',', '.')
                price = Decimal(price_str)
                value_str = row["Valor"].replace('R$', '').strip().replace('.', '').replace(',', '.')
                value = Decimal(value_str)

                TradeOperation.objects.create(
                    trade_date=trade_date,
                    operation=operation,
                    market=market,
                    due_date=due_date,
                    institution=institution,
                    ticker=ticker,
                    quantity=quantity,
                    price=price,
                    value=value,
                )
            except (ValueError, KeyError) as e:
                raise ValidationError(f"Invalid data in row: {row}. Error: {e}")

