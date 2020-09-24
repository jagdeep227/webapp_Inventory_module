from django.contrib import admin

# Register your models here.

from .models import Customer_cart_added1,Customer_cart_checkedout1,admin_company,Employee,Product_variety,Product,Customer,Product_checkout,Product_log,Product_variety_added,Product_variety_checkout

admin.site.register(admin_company)
admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(Product_variety)
admin.site.register(Customer)

admin.site.register(Product_checkout)
admin.site.register(Product_log)
admin.site.register(Product_variety_added)
admin.site.register(Product_variety_checkout)
admin.site.register(Customer_cart_added1)
admin.site.register(Customer_cart_checkedout1)