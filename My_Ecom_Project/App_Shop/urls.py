from django.urls import  path
from App_Shop import views

app_name='App_Shop'

urlpatterns=[
    path('', views.home, name='home'),
    path('product/<pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('search_items/', views.search_items, name='search_items'),
]
