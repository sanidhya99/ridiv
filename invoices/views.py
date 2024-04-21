from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from .renderers import *
from .models import *
from rest_framework import generics,status

class InvoiceCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    renderer_classes = [InvoiceRenderer,]
    queryset=Invoice.objects.all()
    def post(self, request, *args, **kwargs):

        data = request.data

        invoice_data = {
            'customer_name': data.get('customer_name')
        }

        invoice_serializer = InvoiceSerializer(data=invoice_data)

        if invoice_serializer.is_valid():
            invoice_instance = invoice_serializer.save()

            invoice_details_data = {
                'invoice': invoice_instance.pk,  
                'description': data.get('description'),
                'quantity': data.get('quantity'),
                'unit_price': data.get('unit_price'),
                'price': data.get('price')
            }

            # Create an InvoiceDetails instance associated with the Invoice
            invoice_details_serializer = InvoiceDetailsSerializer(data=invoice_details_data)
            if invoice_details_serializer.is_valid():
                invoice_details_serializer.save()
                return Response({"invoice": invoice_instance.pk, "invoice_details": invoice_details_serializer.data}, status=status.HTTP_201_CREATED)

            else:
                # If InvoiceDetails data is not valid, delete the created Invoice instance
                invoice_instance.delete()
                return Response(invoice_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class InvoiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    renderer_classes = [InvoiceRenderer,]
    lookup_field='id'
    queryset=Invoice.objects.all()
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get associated InvoiceDetails for the Invoice instance
        invoice_details = InvoiceDetails.objects.filter(invoice=instance)
        invoice_details_serializer = InvoiceDetailsSerializer(invoice_details, many=True)

        return Response({"invoice": serializer.data, "invoice_details": invoice_details_serializer.data})

    def patch(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        try:
            invoice = Invoice.objects.get(id=id)
            invoice_detail = InvoiceDetails.objects.get(invoice=invoice.pk)
    
            if "customer_name" in request.data:
                customer_name = request.data.get('customer_name')
                invoice.customer_name = customer_name
            if "description" in request.data:
                description = request.data.get('description')
                invoice_detail.description = description
            if "quantity" in request.data:
                quantity = request.data.get('quantity')
                invoice_detail.quantity = quantity
            if "unit_price" in request.data:
                unit_price = request.data.get('unit_price')
                invoice_detail.unit_price = unit_price
            if "price" in request.data:
                price = request.data.get('price')
                invoice_detail.price = price
            
            invoice_detail.save()
            invoice.save()
    
            # Serialize the updated invoice object
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
           