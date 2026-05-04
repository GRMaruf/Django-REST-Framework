from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from app_base.models import *
from app_base.serializers import *


@api_view(['GET'])
def get_product_list(request):
    product_list = ProductInfo.objects.all()
    data = ProductSerializers(product_list, many = True)
    return Response({
        'success': True,
        'message': 'All data collected successfully.',
        'data': data.data
    }, HTTP_200_OK)

@api_view(['GET'])
def get_product(request, pk):
    try:
        product = ProductInfo.objects.get(id = pk)
    except ProductInfo.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Data not found for the PK.',
        }, HTTP_404_NOT_FOUND)
    data = ProductSerializers(product)
    return Response({
        'success': True,
        'message': 'One data collected successfully.',
        'data': data.data
    }, HTTP_200_OK)

@api_view(['POST'])
def create_product(request):
    product = ProductSerializers(data = request.data)
    if product.is_valid():
        product.save()
        return Response({
            'success': True,
            'message': 'One data created successfully.',
            'data': product.data
        }, HTTP_201_CREATED)
    return Response({
        'success': False,
        'message': 'Invalid Data.',
        'error': product.errors
    }, HTTP_406_NOT_ACCEPTABLE)

@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = ProductInfo.objects.get(id = pk)
    except ProductInfo.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Data not found for the PK.',
        }, HTTP_404_NOT_FOUND)
    product = ProductSerializers(product, data = request.data, partial = True)
    # if partial is set to True, you must give all the fields while updating
    # you can live the fields blank, if you want to keep the previous value for numbers or floats
    if product.is_valid():
        product.save()
        return Response({
            'success': True,
            'message': 'One data updated successfully.',
            'data': product.data
        }, HTTP_202_ACCEPTED)
    return Response({
        'success': False,
        'message': 'Invalid Data.',
        'error': product.errors
    }, HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = ProductInfo.objects.get(id = pk)
    except ProductInfo.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Data not found for the PK.',
        }, HTTP_404_NOT_FOUND)
    title = product.title
    product.delete()
    return Response({
        'success': True,
        'product': title,
        'message':'One data deleted successfully.'
    }, HTTP_200_OK)

from rest_framework.views import APIView

class ProductAPI(APIView):
    # method implementations are same as Function Based

    def get(self, request):
        product_list = ProductInfo.objects.all()
        data = ProductSerializers(product_list, many = True)
        return Response({
            'success': True,
            'message': 'All data collected successfully.',
            'data': data.data
        }, HTTP_200_OK)
    
    def get(self, request, pk):
        try:
            product = ProductInfo.objects.get(id = pk)
        except ProductInfo.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Data not found for the PK.',
            }, HTTP_404_NOT_FOUND)
        data = ProductSerializers(product)
        return Response({
            'success': True,
            'message': 'One data collected successfully.',
            'data': data.data
        }, HTTP_200_OK)
    
    def post(self, request):
        product = ProductSerializers(data = request.data)
        if product.is_valid():
            product.save()
            return Response({
                'success': True,
                'message': 'One data created successfully.',
                'data': product.data
            }, HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Invalid Data.',
            'error': product.errors
        }, HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, pk):
        try:
            product = ProductInfo.objects.get(id = pk)
        except ProductInfo.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Data not found for the PK.',
            }, HTTP_404_NOT_FOUND)
        product = ProductSerializers(product, data = request.data, partial = True)
        # if partial is set to True, you must give all the fields while updating
        # you can live the fields blank, if you want to keep the previous value for numbers or floats
        if product.is_valid():
            product.save()
            return Response({
                'success': True,
                'message': 'One data updated successfully.',
                'data': product.data
            }, HTTP_202_ACCEPTED)
        return Response({
            'success': False,
            'message': 'Invalid Data.',
            'error': product.errors
        }, HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self, resuest, pk):
        try:
            product = ProductInfo.objects.get(id = pk)
        except ProductInfo.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Data not found for the PK.',
            }, HTTP_404_NOT_FOUND)
        title = product.title
        product.delete()
        return Response({
            'success': True,
            'product': title,
            'message':'One data deleted successfully.'
        }, HTTP_200_OK)
    
from rest_framework.viewsets import ModelViewSet

class ProductModelViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductSerializers

class ImageModelViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializers
