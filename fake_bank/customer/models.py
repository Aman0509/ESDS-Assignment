from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

acc_type = (
    ('Savings', 'Savings'),
    ('Current', 'Current'),
    ('Loan', 'Loan'))

class customers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    age = models.IntegerField()

    def __str__(self):
        return str(self.id)+"-" + self.first_name + " " + self.last_name


class customeraccounts(models.Model):
    account_num = models.CharField(max_length=5, primary_key=True)
    account_type = models.CharField(max_length=10, choices=acc_type, default='Savings')
    balance = models.FloatField(default=1000.00, validators=[MinValueValidator(1000)])
    nominee = models.CharField(max_length=30)
    customer = models.ForeignKey(customers, on_delete=models.CASCADE)


    