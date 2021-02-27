from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from customer.models import customers, customeraccounts, accounttransaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import customersSerializers, customeraccountsSerializers, accounttransactionSerializer
import datetime as dt

# Create your views here.
@login_required
def apihome(request):
    return render(request, 'apiview/apihome.html')


class customersList(APIView):

    @method_decorator(login_required)
    def get(self, request):
        cust = customers.objects.all()
        serializer1 = customersSerializers(cust, many=True)
        return Response(serializer1.data)


class customerAccountsList(APIView):

    @method_decorator(login_required)
    def get(self, request):
        cust_acc = customeraccounts.objects.all()
        serializer2 = customeraccountsSerializers(cust_acc, many=True)
        return Response(serializer2.data)


@login_required
@api_view(['GET'])
def getbalance(request, pk):
    try:
        acc = customeraccounts.objects.get(account_num=pk)
    except customeraccounts.DoesNotExist:
        return Response({"error": f"Account Number {pk} does not exist in our database"},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = customeraccountsSerializers(acc, many=False)
        return Response(serializer.data)


@login_required
@api_view(['POST'])
def createcustomerrecord(request):
    if request.method == 'POST':
        serializer = customersSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def createnewaccount(request):
    date_ = dt.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    if request.method == 'POST':
        serializer = customeraccountsSerializers(data=request.data)
        amount = request.data['balance']
        acc_num = request.data['account_num']
        if serializer.is_valid():
            serializer.save()
            acc_num_created = customeraccounts.objects.get(account_num=acc_num)
            first_trans_entry = accounttransaction(date=date_, pri_acc_num=acc_num_created, sec_acc_num='cash', amount_credit=amount, curr_bal=amount)
            first_trans_entry.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def transfermoney(request):

    if request.method == 'POST':
        date_ = dt.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        temp_list = []
        withs_acc_num = request.data['with_acc_num']
        trans_acc_num = request.data['tran_acc_num']
        amount = float(request.data['amount'])
        try:
            with_acc_num = customeraccounts.objects.get(account_num=withs_acc_num)
        except customeraccounts.DoesNotExist:
            temp_list.append(with_acc_num) 
        try:
            tran_acc_num = customeraccounts.objects.get(account_num=trans_acc_num)
        except customeraccounts.DoesNotExist:
            temp_list.append(trans_acc_num)
            

        if len(temp_list) == 0:
            if amount > with_acc_num.balance:
                return Response(
                    {"error": "Withdrawl Account has low balance"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif amount == 0:
                return Response(
                    {"error": "Transfer Amount cannot be zero"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif with_acc_num == tran_acc_num:
                return Response(
                    {"detail": "Withdrawl and Deposit Account cannot be same"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                with_acc_num.balance -= amount
                tran_acc_num.balance += amount
                with_acc_num.save()
                tran_acc_num.save()
                with_acc_txn = accounttransaction(date=date_, pri_acc_num=with_acc_num, sec_acc_num=trans_acc_num, amount_debit=amount, curr_bal=with_acc_num.balance)
                depo_acc_txn = accounttransaction(date=date_, pri_acc_num=tran_acc_num, sec_acc_num=withs_acc_num, amount_credit=amount, curr_bal=tran_acc_num.balance)
                with_acc_txn.save()
                depo_acc_txn.save()
                return Response(
                    {'success': 'Transaction Successful'},
                    status=status.HTTP_200_OK
                )
        else:
            if len(temp_list) == 1:
                return Response({"error": f"Account Number {temp_list[0]} does not exist in our database"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": f"Account Number {temp_list[0]} and {temp_list[1]} do not exist in our database"},status=status.HTTP_404_NOT_FOUND)



@login_required
@api_view(['GET'])
def transactionhistory(request, pk):
    
    try:
        acc = customeraccounts.objects.get(account_num=pk)
        tran_history = accounttransaction.objects.filter(pri_acc_num=pk)
    except customeraccounts.DoesNotExist:
        return Response({"error": f"Account Number {pk} does not exist in our database"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = accounttransactionSerializer(tran_history, many=True)
        return Response(serializer.data)

