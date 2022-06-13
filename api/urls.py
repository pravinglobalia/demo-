from django.conf import settings
from django.contrib import admin
from django.urls import path

from ecom.settings import MEDIA_URL
from .import views

from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('singup/', views.singup,name="singup"),
    path('logout/',views.user_logout,name="user_logout"),
    path('forget/',views.change_password,name="change_password"),
    path('products/', views.products,name="products"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    # path('demo/',views.demo,name="demo"),
    path('add_product/',views.add_product,name="add_product"),
    path('info/<int:pk>',views.info,name="info"),
    path('addtocart/',views.addtocart,name="addtocart"),
    path('removecart/',views.removecart,name="removecart"),
    path('cart/',views.cart,name="cart"),
    path('pluscart/<id>/',views.pluscart,name="pluscart"),
    path('minuscart/<id>/',views.minuscart,name="minuscart"),
    path('search/',views.search,name="search"),
    path('checkout/',views.checkout,name="checkout"),
    path('success/',views.success,name="success"),
    path('failed/',views.failed,name="failed"),
    path('api/checkout-session/<id>/',views.create_checkout_session,name="api_checkout_session")




]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
