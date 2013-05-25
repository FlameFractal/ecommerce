from django.contrib import admin
from models import *

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('user', 'address', 'payment', 'order_total')

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Advertisement)