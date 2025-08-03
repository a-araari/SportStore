from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_list, name='order_list'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]