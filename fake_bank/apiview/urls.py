from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.apihome, name='apispage'),
    path('apicustomercreation/', views.createcustomerrecord, name='apicustomercreation'),
    path('apinewaccountcreation/', views.createnewaccount, name='apinewaccountcreation'),
    path('apitransfermoney/', views.transfermoney, name='apitransfermoney'),
    path('apibal/<str:pk>/', views.getbalance, name='apibal'),
    path('apitransactionhistory/<str:pk>/', views.transactionhistory, name='apitransactionhistory'),
    path('apiviewofallcustomers/', views.customersList.as_view(), name='apiviewofallcustomers'),
    path('apiviewofallaccounts/', views.customerAccountsList.as_view(), name='apiviewofallaccounts'),
]
