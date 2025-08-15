from django.db import models

class Report(models.Model):
    report = models.FileField(upload_to='media/reports/')

