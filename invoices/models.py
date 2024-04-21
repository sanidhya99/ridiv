from django.db import models
import datetime

class Invoice(models.Model):
    date = models.DateField(default=datetime.date.today)
    customer_name = models.CharField(max_length=100)

class InvoiceDetails(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)    
    description = models.CharField(max_length=1000)
    quantity = models.BigIntegerField()
    unit_price = models.FloatField()
    price=models.FloatField()

    def __str__(self):
        return self.invoice.customer_name
