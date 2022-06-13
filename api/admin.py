from django.contrib import admin
from .models import Item,Cart,Contact,Order,OrderItem,OrderDetail
# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderDetail)

