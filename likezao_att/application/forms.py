from django import forms

from .models import BankDetail, User, Rule, Var

class BankDetailForm(forms.ModelForm):  
    class Meta:  
        model = BankDetail
        fields = ['branch', 'account_number', 'name', 'account_type', 'bank_number']
        
class UserForm(forms.ModelForm):
    class Meta:  
        model = User
        fields = ['cpf', 'full_name', 'email', 'phone', 'maximum_earning_per_day']

class RuleForm(forms.ModelForm):  
    class Meta:  
        model = Rule
        fields = ['minimum_withdrawl', 'maximum_earning_per_day', 'minimum_per_click', 'maximum_per_click']

class VarForm(forms.ModelForm):  
    class Meta:  
        model = Var
        fields = ['number_star']
        