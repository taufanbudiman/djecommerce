from django.urls import path
from .views import (
    item_list,
    checkout,
    product,
    HomeView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-to-cart/<slug>/', remove_from_cart, name='remove-to-cart'),
]