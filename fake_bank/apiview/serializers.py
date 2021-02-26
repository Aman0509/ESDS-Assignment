from rest_framework import serializers
from customer.models import customers, customeraccounts

class customersSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = customers
        fields = '__all__'


class customeraccountsSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = customeraccounts
        fields = "__all__"


