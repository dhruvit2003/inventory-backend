from rest_framework import serializers
from .models import Item, BuyingTransaction, SellingTransaction

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'no_of_available_item']

class BuyingTransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = BuyingTransaction
        fields = ['id', 'item', 'item_name', 'no_of_item', 'price_of_one_piece', 'total_rupees', 'date_created']
        read_only_fields = ['total_rupees', 'date_created']

class SellingTransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = SellingTransaction
        fields = ['id', 'item', 'item_name', 'no_of_item', 'price_of_one_piece', 'total_rupees', 'date_created']
        read_only_fields = ['total_rupees', 'date_created']