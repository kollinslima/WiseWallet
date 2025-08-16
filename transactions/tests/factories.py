import tempfile
import string
import random
import factory
from factory import fuzzy
from pathlib import Path
from abc import ABC, abstractmethod

from transactions.models import B3TransactionReports

class B3TransactionReportsFactory(factory.django.DjangoModelFactory):                           
    class Meta:                                                                 
        model = B3TransactionReports                            
                                                                                
    report = factory.django.FileField(filename=fuzzy.FuzzyText(length=100, suffix=".csv"))

class CsvFactory(ABC):
    @abstractmethod
    def create_batch(size=1, path=tempfile.gettempdir()):
        base_path = Path(path)
        base_path.mkdir(parents=True, exist_ok=True)
        extension=".csv"
        created_files = []
        
        for i in range(size):
            file_name = ''.join([random.choice(string.ascii_letters) for _i in range(100)])+".csv"
            file_path = base_path.joinpath(Path(file_name))
            file_path.touch()
            created_files.append(file_path)

        return created_files



