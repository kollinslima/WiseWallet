from .models import Transaction
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

class TransactionsFileUploadTest(TestCase):
    def test_upload_non_csv_file(self):
        url = reverse('transactions')
        file_content = b'This is a test file.'
        uploaded_file = SimpleUploadedFile('test.txt', file_content, content_type='text/plain')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'file_field', 'Cannot open CSV file.')

    def test_upload_csv_file(self):
        url = reverse('transactions')
        file_content = b'"Data do Neg\xc3\xb3cio","Tipo de Movimenta\xc3\xa7\xc3\xa3o","Mercado","Prazo/Vencimento","Institui\xc3\xa7\xc3\xa3o","C\xc3\xb3digo de Negocia\xc3\xa7\xc3\xa3o","Quantidade","Pre\xc3\xa7o","Valor"\n"01/01/2023","Compra","A vista","-","Corretora","PETR4",100,"R$25,00","R$2.500,00"\n'
        uploaded_file = SimpleUploadedFile('test.csv', file_content, content_type='text/csv')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/transactions/upload/success')

    def test_atomic_upload_with_invalid_row(self):
        url = reverse('transactions')
        file_content = b'"Data do Neg\xc3\xb3cio","Tipo de Movimenta\xc3\xa7\xc3\xa3o","Mercado","Prazo/Vencimento","Institui\xc3\xa7\xc3\xa3o","C\xc3\xb3digo de Negocia\xc3\xa7\xc3\xa3o","Quantidade","Pre\xc3\xa7o","Valor"\n"01/01/2023","Compra","A vista","-","Corretora","PETR4",100,"R$25,00","R$2.500,00"\n"invalid-date","Compra","A vista","-","Corretora","PETR4",100,"R$25,00","R$2.500,00"\n'
        uploaded_file = SimpleUploadedFile('test.csv', file_content, content_type='text/csv')

        response = self.client.post(url, {'file_field': uploaded_file})

        self.assertEqual(response.status_code, 200)
        expected_error = "Invalid data in row: {'Data do Negócio': 'invalid-date', 'Tipo de Movimentação': 'Compra', 'Mercado': 'A vista', 'Prazo/Vencimento': '-', 'Instituição': 'Corretora', 'Código de Negociação': 'PETR4', 'Quantidade': '100', 'Preço': 'R$25,00', 'Valor': 'R$2.500,00'}. Error: time data 'invalid-date' does not match format '%d/%m/%Y'"
        self.assertFormError(response.context['form'], 'file_field', expected_error)
        self.assertEqual(Transaction.objects.count(), 0)
