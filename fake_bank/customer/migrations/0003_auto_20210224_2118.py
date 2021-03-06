# Generated by Django 3.1.5 on 2021-02-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20210224_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customeraccounts',
            old_name='acc',
            new_name='customer',
        ),
        migrations.AlterField(
            model_name='customeraccounts',
            name='account_type',
            field=models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current'), ('Loan', 'Loan')], default='Savings', max_length=10),
        ),
        migrations.AlterField(
            model_name='customeraccounts',
            name='balance',
            field=models.FloatField(default=1000.0),
        ),
    ]
