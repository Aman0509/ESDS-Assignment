from django.contrib import admin
from customer.models import customers, customeraccounts

# Register your models here.

class customersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


class customeraccountsAdmin(admin.ModelAdmin):
    list_display = ['account_num']



admin.site.register(customers, customersAdmin)
admin.site.register(customeraccounts, customeraccountsAdmin)