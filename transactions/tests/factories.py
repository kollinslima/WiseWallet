import factory
import io
import locale
import openpyxl
import random
import string

from factory import fuzzy
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from transactions.models import TransactionOperations, TransactionInstitutions, AssetClassification, AssetIdentification
from tests.factories import UserFactory

class AssetClassificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssetClassification

    user = factory.SubFactory(UserFactory)
    asset_type = fuzzy.FuzzyText(length=100)

class AssetIdentificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssetIdentification

    user = factory.SubFactory(UserFactory)
    asset_ticker = factory.Sequence(lambda n: f"TICKER_{n:03}")
    asset_name = fuzzy.FuzzyText(length=100)
    asset_classification = factory.LazyAttribute(
        lambda obj: AssetClassificationFactory(user=obj.user)
    )

class TransactionInstitutionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionInstitutions

    user = factory.SubFactory(UserFactory)
    name = fuzzy.FuzzyText(length=100)

class TransactionOperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionOperations

    user = factory.SubFactory(UserFactory)
    asset = factory.LazyAttribute(
        lambda obj: AssetIdentificationFactory(user=obj.user)
    )
    institution_name = factory.LazyAttribute(
        lambda obj: TransactionInstitutionsFactory(user=obj.user)
    )
    operation = fuzzy.FuzzyChoice([choice[0] for choice in TransactionOperations.TransactionOperation.choices])
    operation_date = fuzzy.FuzzyDate(date(2008, 1, 1))
    settlement_date = fuzzy.FuzzyDate(date(2008, 1, 1))
    amount = fuzzy.FuzzyInteger(0, 999999999999)
    total_value = fuzzy.FuzzyDecimal(0.0, 99999999.99, 2)
    fees = fuzzy.FuzzyDecimal(0.0, 99999999.99, 2)
    

class B3TransactionsFileFactory(SimpleUploadedFile):
    def __init__(self, num_of_transactions=12, header=None, content=None):
        name = f"{self._generate_random_string(10)}.xlsx"
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        _content = []

        if header is not None:
            _header = header
        else:
            _header = ["Entrada/Saída", "Data", "Movimentação", "Produto", "Instituição", "Quantidade", "Preço unitário", "Valor da Operação"]

        _content.append(_header)

        if content is not None:
            _content.extend(content)
        else:

            original_locale = locale.getlocale()
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

            today = date.today()
            start_date = today - timedelta(days=3 * 365)
            days_between_dates = (today - start_date).days

            for i in range(num_of_transactions):
                row = []
                row.append(random.choice(["Debito", "Credito"]))

                random_number_of_days = random.randrange(days_between_dates)
                random_date = start_date + timedelta(days=random_number_of_days)
                row.append(random_date.strftime('%d/%m/%Y'))

                row.append("Transferência - Liquidação")

                ticker_endings = random.choice(["3", "4", "11"])
                row.append(f"{self._generate_random_string(4)}{ticker_endings} - {self._generate_random_string(50)}")
                row.append(self._generate_random_string(100))
                amount = random.uniform(1, 1000)
                row.append(amount)
                unit_price = round(random.uniform(1.0, 1000.0),2)
                row.append(f"{locale.currency(unit_price, grouping=True)}")
                row.append(f"{locale.currency(amount*unit_price, grouping=True)}")
                _content.append(row)

            locale.setlocale(locale.LC_ALL, original_locale)

        _file_content = self._create_xlsx_content(_content)
        super().__init__(name, _file_content.read(), content_type)

    def _create_xlsx_content(self, data):
        output = io.BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        for row_data in data:
            sheet.append(row_data)
            
        workbook.save(output)
        output.seek(0)
        return output

    def _generate_random_string(self, length):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))
