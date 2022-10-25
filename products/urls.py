from django.urls import path

from products.views import ProductDetailView, ProductView

urlpatterns = [
    path(
        "products/",
        ProductView.as_view(),
    ),
    path(
        "products/<pk>/",
        ProductDetailView.as_view(),
    ),
]
