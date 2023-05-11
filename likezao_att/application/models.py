from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class User(AbstractUser):
  cpf = models.CharField(max_length=11, unique=True)
  full_name = models.CharField(max_length=100)
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  today_earning = models.DecimalField(default=0, max_digits=7, decimal_places=2)
  maximum_earning_per_day = models.FloatField(default=200)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class BankDetail(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_details')
  ACCOUNT_TYPES = [('Current', 'Current'), ('Saving', 'Saving')]
  branch = models.CharField(max_length=100, default="")
  account_number = models.CharField(max_length=50, default="")
  name = models.CharField(max_length=100, default="")
  account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default="Current")
  bank_number = models.CharField(max_length=50, default="")
  total_earning = models.DecimalField(default=0, max_digits=7, decimal_places=2)
  additional_information = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Rule(models.Model):
  minimum_withdrawl = models.FloatField(default=500)
  maximum_earning_per_day = models.FloatField(default=50)
  minimum_per_click = models.FloatField(default=0.1)
  maximum_per_click = models.FloatField(default=5)

class Var(models.Model):
  number_star = models.IntegerField(default=3)
  