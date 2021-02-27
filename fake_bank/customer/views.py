from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import customersForm, customeraccountsForm
from .models import customers, customeraccounts, accounttransaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import datetime as dt

# UI Views

@login_required
def accountcreation(request):
    return render(request, 'customer/accountcreation.html')


@login_required
def transfer(request):
    
    if request.method == 'POST':
        temp_list = []
        date_ = dt.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        with_acc_num = request.POST['with_acc_num']
        trans_acc_num = request.POST['trans_acc_num']
        amount = float(request.POST['amount'])
        # Checking whether the Account numbers exist in out database
        try:
            temp_with_acc = customeraccounts.objects.get(account_num__contains=with_acc_num)
        except ObjectDoesNotExist:
            temp_list.append(with_acc_num)
        
        try:
            temp_trans_acc = customeraccounts.objects.get(account_num__contains=trans_acc_num)
        except ObjectDoesNotExist:
            temp_list.append(trans_acc_num)
        
        if len(temp_list) == 0: 
            # Checking whether there is enough balance in withdrawl account
            if amount == 0:
                messages.error(request, 'Transfer amount cannot be 0')
                return redirect('transfer')
            elif temp_with_acc.balance < amount:
                messages.error(request, f'{with_acc_num} has low balance')
                return redirect('transfer')
            elif with_acc_num == trans_acc_num:
                messages.error(request, f'Withdrawl and Deposit accounts cannot be same')
                return redirect('transfer')
            else:
                temp_with_acc.balance -= amount
                temp_trans_acc.balance += amount
                temp_with_acc.save()
                temp_trans_acc.save()
                with_acc_txn = accounttransaction(date=date_, pri_acc_num=temp_with_acc, sec_acc_num=trans_acc_num, amount_debit=amount, curr_bal=temp_with_acc.balance)
                depo_acc_txn = accounttransaction(date=date_, pri_acc_num=temp_trans_acc, sec_acc_num=with_acc_num, amount_credit=amount, curr_bal=temp_trans_acc.balance)
                with_acc_txn.save()
                depo_acc_txn.save()
                message = f'Rs {amount} has been transferred to account {trans_acc_num}'
                return render(request, 'customer/transfer.html', {'message': message})
        else:
            if len(temp_list) == 1:
                msg = f'Account {temp_list[0]} does not exist in our database'
            if len(temp_list) == 2:
                msg = f'Account {temp_list[0]} and {temp_list[1]} do not exist in our database' 
            messages.error(request, msg)
            return redirect('transfer')
    
    return render(request, 'customer/transfer.html')


@login_required
def checkbalance(request):
    if request.method == "POST":
        acc_num = request.POST["acc_num"]
        try:
            temp = customeraccounts.objects.get(account_num__contains=acc_num)
            return render(request, 'customer/checkbalance.html', {'temp': temp})
        except ObjectDoesNotExist:
            temp = None
            messages.error(request, f'{acc_num} does not exist')
            return redirect('checkbal')
    else:
        return render(request, 'customer/checkbalance.html')
    

@login_required
def transactionhistory(request):
    if request.method == "POST":
        acc_num = request.POST["acc_num"]
        try:
            temp = customeraccounts.objects.get(account_num__contains=acc_num)
            transaction_table = accounttransaction.objects.filter(pri_acc_num=acc_num)
            return render(request, 'customer/transactionhistory.html', {'trans_table': transaction_table})
        except ObjectDoesNotExist:
            temp = None
            messages.error(request, f'{acc_num} does not exist')
            return redirect('t_history')
    return render(request, 'customer/transactionhistory.html')


@login_required
def newcustomer(request):
    form = customersForm()
    if request.method == "POST":
        form = customersForm(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data['first_name']
            messages.success(request, f'Customer Record Created for {cust_name}')
            form.save()
            return redirect('new_cust')
    else:
        form = customersForm()
    return render(request, 'customer/newcustomer.html', {'form': form })


@login_required
def newaccount(request):
    date_ = dt.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    form = customeraccountsForm()
    if request.method == "POST":
        form = customeraccountsForm(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data['customer']
            acc_type = form.cleaned_data['account_type']
            acc_num = form.cleaned_data['account_num']
            acc_bal = form.cleaned_data['balance']
            messages.success(request, f'{acc_type} account number {acc_num} is opened for {cust_name}')
            form.save()
            acc_num = customeraccounts.objects.get(account_num=acc_num)
            first_trans_entry = accounttransaction(date=date_, pri_acc_num=acc_num, sec_acc_num='cash', amount_credit=acc_bal, curr_bal=acc_bal)
            first_trans_entry.save()
            return redirect('acc_open')
    else:
        form = customeraccountsForm()
    return render(request, 'customer/newaccountcreation.html', {'form': form })


