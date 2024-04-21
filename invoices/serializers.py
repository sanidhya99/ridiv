from rest_framework import serializers
from .models import *


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        details = InvoiceDetails.objects.filter(invoice=instance)
        representation['details'] = InvoiceDetailsSerializer(details, many=True).data
        return representation    
class InvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = '__all__'
