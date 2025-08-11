import io
import openpyxl

from .models import TradeOperation
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

class TransactionsFileUploadTest(TestCase):
    def _create_xlsx_file(self, data):
        output = io.BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        for row_data in data:
            sheet.append(row_data)
            
        workbook.save(output)
        output.seek(0)
        return output

    def test_upload_non_xlsx_file(self):
        url = reverse('transactions')
        file_content = b'This is a test file.'
        uploaded_file = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'file_field', 'Invalid file format. Please upload a .xlsx file.')

    def test_upload_xlsx_file(self):
        url = reverse('transactions')
        header = ["Data do Negócio", "Tipo de Movimentação", "Mercado", "Prazo/Vencimento", "Instituição", "Código de Negociação", "Quantidade", "Preço", "Valor"]
        row = ["01/01/2023", "Compra", "A vista", "-", "Corretora", "PETR4", 100, "R$25,00", "R$2.500,00"]
        
        file_content = self._create_xlsx_file([header, row])
        uploaded_file = SimpleUploadedFile('test.xlsx', file_content.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/transactions/upload/success')

    def test_atomic_upload_with_invalid_row(self):
        url = reverse('transactions')
        header = ["Data do Negócio", "Tipo de Movimentação", "Mercado", "Prazo/Vencimento", "Instituição", "Código de Negociação", "Quantidade", "Preço", "Valor"]
        valid_row = ["01/01/2023", "Compra", "A vista", "-", "Corretora", "PETR4", 100, "R$25,00", "R$2.500,00"]
        invalid_row = ["invalid-date", "Compra", "A vista", "-", "Corretora", "PETR4", 100, "R$25,00", "R$2.500,00"]

        file_content = self._create_xlsx_file([header, valid_row, invalid_row])
        uploaded_file = SimpleUploadedFile('test.xlsx', file_content.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 200)
        expected_error_substring = "Invalid data in row"
        form_error = response.context['form'].errors['file_field'][0]
        self.assertTrue(expected_error_substring in form_error)
        self.assertEqual(TradeOperation.objects.count(), 0)
