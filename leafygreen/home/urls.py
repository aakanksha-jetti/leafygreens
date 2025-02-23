from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('add_to_cart/<int:veggie_id>/', views.add_to_cart, name='add_to_cart'),
]
