from rest_framework import serializers
from app_base.models import *

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        
        # suppose, product_id is username + id
        username = "maruf"
        id = instance.id
        instance.product_id = f'{username}_{id}'
        instance.save()

        return instance

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'