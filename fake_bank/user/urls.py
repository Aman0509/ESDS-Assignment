from django.urls import path, include
from . import views
from customer import views as cust_views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('newacc/', cust_views.accountcreation, name='new-acc'),
    path('transfer/', cust_views.transfer, name='transfer'),
    path('checkbal/', cust_views.checkbalance, name='checkbal'),
    path('transhist/', cust_views.transactionhistory, name='t_history'),
    path('newcust/', cust_views.newcustomer, name='new_cust'),
    path('accopen/', cust_views.newaccount, name='acc_open'),
]
