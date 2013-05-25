from django.contrib import admin
from models import *

class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    fk_name = "order"
    extra = 0
    readonly_fields = ('quantity', 'product')

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemsInline,
    ]
    readonly_fields = ('user', 'address', 'payment', 'order_total')

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('items_sold', )

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Advertisement)