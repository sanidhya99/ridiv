from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from .renderers import *
from .models import *
from rest_framework import generics,status

class InvoiceCreateAPIView(generics.CreateAPIView):
    serializer_class = InvoiceSerializer
    renderer_classes = [InvoiceRenderer,]

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

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get associated InvoiceDetails for the Invoice instance
        invoice_details = InvoiceDetails.objects.filter(invoice=instance)
        invoice_details_serializer = InvoiceDetailsSerializer(invoice_details, many=True)

        return Response({"invoice": serializer.data, "invoice_details": invoice_details_serializer.data})

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update associated InvoiceDetails if related fields are present in request data
        if 'description' in request.data or 'quantity' in request.data or 'unit_price' in request.data or 'price' in request.data:
            invoice_details = InvoiceDetails.objects.filter(invoice=instance)
            invoice_details_data = {
                'description': request.data.get('description', instance.invoice_details.description),
                'quantity': request.data.get('quantity', instance.invoice_details.quantity),
                'unit_price': request.data.get('unit_price', instance.invoice_details.unit_price),
                'price': request.data.get('price', instance.invoice_details.price)
            }
            invoice_details_serializer = InvoiceDetailsSerializer(invoice_details, data=invoice_details_data, partial=partial)
            if invoice_details_serializer.is_valid():
                invoice_details_serializer.save()

        return Response(serializer.data)