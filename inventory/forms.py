from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

CON=(
    ("0","select"),
    ("1","India"),
    ("2","USA"),
)
STATES=(
("0","select"),
("1","Andhra Pradesh"),
("2","Arunachal Pradesh"),
("3","Assam"),
("4","Bihar"),
("5","Chhattisgarh"),
("6","Goa"),
("7","Gujarat"),
("8","Haryana"),
("9","Himachal Pradesh"),
("10","Jharkhand"),
("11","Karnataka"),
("12","Kerala"),
("13","Madhya Pradesh"),
("14","Maharashtra"),
("15","Manipur"),
("16","Meghalaya"),
("17","Mizoram"),
("18","Nagaland"),
("19","Odisha"),
("20","Punjab"),
("21","Rajasthan"),
("22","Sikkim"),
("23","Tamil Nadu"),
("24","Telangana"),
("25","Tripura"),
("26","Uttarakhand"),
("27","Uttar Pradesh"),
("28","West Bengal"),
)

class DateInput(forms.DateInput):
    input_type = 'date'


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:    
        fields = ['start_date','end_date']
        
class SearchForm(forms.Form):
    product_name=forms.CharField(max_length=200)
    min_quantity=forms.IntegerField()
    class Meta:    
        fields=['product_name','min_quantity']

class RegistrationFormUser(UserCreationForm):
    name=forms.CharField(max_length=200)                
    phone=forms.CharField(max_length=20)
    username=forms.CharField(max_length=20)    
    email1=forms.EmailField()

    class Meta:
        model = User
        fields = ['name','username','phone','email1', 'password1', 'password2']


class Add_CustomerForm(UserCreationForm): 
    name=forms.CharField(max_length=200)                
    phone=forms.CharField(max_length=20)
    username=forms.CharField(max_length=20)    
    email1=forms.EmailField()
    address=forms.CharField(max_length=200)   
    class Meta:
        model = User
        fields = ['name','username','phone','email1','address','password1', 'password2']

class Update_CustomerForm(ModelForm):    
    class Meta:
        model = Customer
        fields = ['name','email1','address']



class FindCustomer(forms.Form):    
    username_or_phone=forms.CharField(max_length=200)
    class Meta:
        model = Customer
        fields = ['username_or_phone',]

class AddStock(ModelForm):

    name=forms.CharField(max_length=200)
    Q_CHOICES=(
        ('kg','kg'),
        ('quintal','quintal'),
        ('tonnes','tonnes'),        
        ('not specified','not specified')
    )
    quant_type=forms.ChoiceField(choices=Q_CHOICES)
    class Meta:
        model = Product_variety
        fields = ['name','variety_name','quantity','price_per_unit','quant_type']


class CheckOutStock(ModelForm):

    name=forms.CharField(max_length=200)
    class Meta:
        model = Product_variety
        fields = ['name','variety_name','quantity',]
