from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item, BuyingTransaction, SellingTransaction
from .serializers import ItemSerializer, BuyingTransactionSerializer, SellingTransactionSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class BuyingTransactionViewSet(viewsets.ModelViewSet):
    queryset = BuyingTransaction.objects.all()
    serializer_class = BuyingTransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['item']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Calculate total before saving
        serializer.validated_data['total_rupees'] = (
            serializer.validated_data['no_of_item'] * 
            serializer.validated_data['price_of_one_piece']
        )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SellingTransactionViewSet(viewsets.ModelViewSet):
    queryset = SellingTransaction.objects.all()
    serializer_class = SellingTransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['item']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if enough items are in stock
        item_id = serializer.validated_data['item'].id
        item = Item.objects.get(pk=item_id)
        requested_qty = serializer.validated_data['no_of_item']
        
        if item.no_of_available_item < requested_qty:
            return Response(
                {"detail": f"Not enough items in stock. Available: {item.no_of_available_item}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total before saving
        serializer.validated_data['total_rupees'] = (
            serializer.validated_data['no_of_item'] * 
            serializer.validated_data['price_of_one_piece']
        )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)