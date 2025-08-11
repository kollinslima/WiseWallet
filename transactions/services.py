import openpyxl

from .models import TradeOperation
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction

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
    
    with transaction.atomic():
        for row_index in range(2, sheet.max_row + 1):
            row_values = [cell.value for cell in sheet[row_index]]
            row = dict(zip(header, row_values))
            
            try:
                trade_date = row["Data do Negócio"].date() if isinstance(row["Data do Negócio"], datetime) else datetime.strptime(row["Data do Negócio"], '%d/%m/%Y').date()
                operation = row["Tipo de Movimentação"]
                market = row["Mercado"]
                due_date_str = row["Prazo/Vencimento"]
                due_date = due_date_str.date() if isinstance(due_date_str, datetime) else (datetime.strptime(due_date_str, '%d/%m/%Y').date() if due_date_str and due_date_str != '-' else None)
                institution = row["Instituição"]
                ticker = row["Código de Negociação"]
                quantity = int(row["Quantidade"])
                price_str = str(row["Preço"]).replace('R$', '').strip().replace('.', '').replace(',', '.')
                price = Decimal(price_str)
                value_str = str(row["Valor"]).replace('R$', '').strip().replace('.', '').replace(',', '.')
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
            except (ValueError, KeyError, TypeError) as e:
                raise ValidationError(f"Invalid data in row: {row}. Error: {e}")

