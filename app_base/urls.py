from django.urls import path, include
from app_base.views import *

# for model view set
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product-model', ProductModelViewSet, basename = 'product_model')
router.register(r'image-model', ImageModelViewSet, basename = 'image_model')

urlpatterns = [
    path('get-product-list', get_product_list),
    path('get-product/<int:pk>', get_product),
    path('create-product', create_product),
    path('update-product/<int:pk>', update_product),
    path('delete-product/<int:pk>', delete_product),

    # ------- easy access (Function Based)
    path('product', get_product_list),
    path('product/<int:pk>', get_product),
    path('product/add', create_product),
    path('product/update/<int:pk>', update_product),
    path('product/delete/<int:pk>', delete_product),

    # ------- easy access (Class Based)
    path('product-api', ProductAPI.as_view()),
    path('product-api/<int:pk>', ProductAPI.as_view()),

    # ------ easy access (Class Based - Model View Set)
    path('', include(router.urls))
]