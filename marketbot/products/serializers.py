# products/serializers.py
from rest_framework import serializers
from .models import StoreProduct

class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = '__all__'
