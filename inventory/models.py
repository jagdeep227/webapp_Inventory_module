from django.db import models
from django.contrib.auth.models import Permission, User
import uuid

class admin_company(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200,primary_key=True)
    email1=models.EmailField(max_length=200)
    company_id=models.UUIDField( default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20,unique=True)
    username=models.CharField(max_length=20,primary_key=True)
    email1=models.EmailField(max_length=200)
    company=models.ForeignKey(admin_company,on_delete=models.CASCADE)
    employee_id=models.UUIDField( default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class Customer(models.Model):
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20,unique=True)
    username=models.CharField(max_length=20,primary_key=True)
    address=models.CharField(max_length=300,null=True)
    email1=models.EmailField(max_length=200)    
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rent_due=models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Customer_cart_added1(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200)
    variety_name=models.CharField(max_length=200)
    quant_type=models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return self.name+self.variety_name

class Customer_cart_checkedout1(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200)
    variety_name=models.CharField(max_length=200)
    quant_type=models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return self.name+self.variety_name

class Product(models.Model):
    name=models.CharField(max_length=200)
    product_uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_quant=models.IntegerField(null=True)
    num_varities=models.IntegerField(null=True)
    Q_CHOICES=(
        ('kg','kg'),
        ('quintal','quintal'),
        ('tonnes','tonnes'),        
        ('not specified','not specified')
    )
    quant_type=models.CharField(max_length=100,choices=Q_CHOICES)
    chck=models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Product_variety(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    employee_added=models.ForeignKey(Employee,on_delete=models.CASCADE)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE)
    variety_name=models.CharField(max_length=200,null=True)
    variety_uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity=models.IntegerField()
    price_per_unit=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variety_name


class Product_variety_added(models.Model):
    product=models.CharField(max_length=200,null=True)
    employee_added=models.ForeignKey(Employee,on_delete=models.CASCADE)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE)
    variety_name=models.CharField(max_length=200,null=True)
    variety_uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity=models.IntegerField()
    quant_type=models.CharField(max_length=50,default="kg")
    price_per_unit=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variety_name



class Product_checkout(models.Model):
    name=models.CharField(max_length=200)
    product_uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_quant=models.IntegerField(null=True)
    num_varities=models.IntegerField(null=True)
    Q_CHOICES=(
        ('kg','kg'),
        ('quintal','quintal'),
        ('tonnes','tonnes'),        
        ('not specified','not specified')
    )
    quant_type=models.CharField(max_length=100,choices=Q_CHOICES)
    chck=models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Product_variety_checkout(models.Model):
    Product_checkout=models.ForeignKey(Product_checkout,on_delete=models.CASCADE)
    employee_checkout=models.ForeignKey(Employee,on_delete=models.CASCADE)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE)
    variety_name=models.CharField(max_length=200,null=True)
    variety_uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity=models.IntegerField()
    price_per_unit=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Product_checkout.name+self.variety_name

class Product_log(models.Model):
    product_intial_quant=models.IntegerField(null=True)
    product_net_quant=models.IntegerField(null=True)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    variety_name=models.CharField(max_length=200,null=True)    
    Q_CHOICES=(
        ('kg','kg'),
        ('quintal','quintal'),
        ('tonnes','tonnes'),        
        ('not specified','not specified')
    )
    quant_type=models.CharField(max_length=100,choices=Q_CHOICES)
    added_or_checkedout=models.CharField(max_length=50)
    quantity=models.IntegerField()
    price_per_unit=models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name+self.variety_name
