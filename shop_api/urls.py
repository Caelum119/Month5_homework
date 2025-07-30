
from django.contrib import admin
from django.urls import path, include
from product import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product', views.product_list_api_view),
]
