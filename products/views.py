from rest_framework import generics

from products.models import Product
from products.permissions import HasObjectPermission, HasPermission
from products.serializers import ProductDetailSerializer, ProductSerializer

from rest_framework.authentication import TokenAuthentication

from utils.mixin import SerializerByMethodMixin


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission, HasObjectPermission]
