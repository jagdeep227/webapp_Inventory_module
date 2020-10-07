from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.models import User,Group,auth
from django.contrib import messages
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required                             
import datetime
from .decorators import *
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf #created in step 4
from django.template.loader import get_template

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def base(request):
    print("IN BASE ")
    return render(request,'base.html',{})




@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def base_employee(request):
    print("IN EMPLOYEE BASE")
    return render(request,'base_employee.html',{})



@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('base')
        else:
            messages.warning(request,"Check your Username or Password.")
            return render(request,'login.html',{})
    return render(request,'login.html',{})

def logout(request):
    auth.logout(request)
    print("logging out")
    return redirect('login') 



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_employee(request):
    title="ADD Employee"
    form = RegistrationFormUser
    #print("@@@@@@@@@@@@@@@@",request.method)
    if request.method=="POST":
        form=RegistrationFormUser(request.POST)
        if form.is_valid():
            #print("form ios valid")
            name=form.cleaned_data['name']
            phone=form.cleaned_data['phone']
            username=form.cleaned_data['username']            
            email1=form.cleaned_data['email1']
            company=admin_company.objects.get(user=request.user)            
            user=form.save()
            group = Group.objects.get(name="employee")
            user.groups.add(group)
            Employee.objects.create(user=user,name=name,email1=email1,phone=phone,username=username,company=company)
            message = "New Employee is added with username: "+username
            return render(request, 'base.html', {'display_text': message})
    return render(request, 'add_employee.html', {'form': form, 'title': title})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def add_customer(request):
    title="ADD Customer"
    form = Add_CustomerForm
    print("@@@@@@@@@@@@@@@@",request.method)
    if request.method=="POST":
        form=Add_CustomerForm(request.POST)
        if form.is_valid():
            print("form ios valid")
            name=form.cleaned_data['name']
            phone=form.cleaned_data['phone']
            username=form.cleaned_data['username']            
            email1=form.cleaned_data['email1']            
            address=form.cleaned_data['address']
            user=form.save()
            group = Group.objects.get(name="customer")
            user.groups.add(group)            
            employee=Employee.objects.get(user=request.user)
            Customer.objects.create(user=user,address=address,name=name,phone=phone,username=username,email1=email1,employee=employee)
            message = "New customer is added with username: "+username
            return render(request, 'base_employee.html', {'display_text': message})
    return render(request, 'add_customer.html', {'form': form, 'title': title})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def view_customer(request):
    return render(request,'view_customer.html',{})


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee','admin'])
def view_stock(request,pk):
    cust=Customer.objects.get(username=pk)
    products=Product_variety.objects.filter(owner=cust)
    print(products)
    return render(request,'view_stock.html',{'cust':cust,'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee','admin'])
def product_log(request,pk):
    customer=Customer.objects.get(username=pk)
    log=Product_log.objects.filter(owner=customer).order_by('-created_at')
    
    return render(request,'product_log.html',{'log':log,'cust':customer})



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def home_forcustomer(request):
    cust=Customer.objects.filter(user=request.user)
    return render(request,'customer.html',{'cust':cust})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def view_stock_forcustomer(request,pk):
    cust=Customer.objects.get(username=pk)
    products=Product_variety.objects.filter(owner=cust)
    print(products)
    return render(request,'view_stock_forcustomer.html',{'cust':cust,'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def product_log_forcustomer(request,pk):
    customer=Customer.objects.get(username=pk)
    log=Product_log.objects.filter(owner=customer).order_by('-created_at')
    
    return render(request,'product_log_forcustomer.html',{'log':log,'cust':customer})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def base_customer(request,pk):
    cust=Customer.objects.get(username=pk)
    return render(request,'base_customer.html',{'cust':cust})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def open_customer(request):
    title="See Customer"
    form=FindCustomer
    msg=None
    print("@@@@@@@@@@@@@@@@",request.method)
    if request.method=="POST":
        form=FindCustomer(request.POST)
        if form.is_valid():
            print("form ios valid")            
            username_or_phone=form.cleaned_data['username_or_phone']
            print(username_or_phone,"%%%%%%%%%%%%%%%%%%")
            cust=Customer.objects.filter(Q(username=username_or_phone)|Q(phone=username_or_phone))
            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            if cust:
                return render(request, 'base_customer.html', {'cust':cust[0]})
            msg="Wrong Username or Phone number"
    return render(request, 'open_customer.html', {'form': form, 'title': title,'message':msg})


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def see_customers(request):
    cust=Customer.objects.filter()
    return render(request,'see_customers.html',{'cust':cust})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def see_customers_admin(request):
    cust=Customer.objects.filter()
    return render(request,'see_customer_admin.html',{'cust':cust})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def see_employees(request):
    cust=Employee.objects.filter()
    return render(request,'see_employees.html',{'cust':cust})



@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def add_stock(request,pk):
    cust=Customer.objects.get(username=pk)
    employee=Employee.objects.get(user=request.user)
    form=AddStock
    prods=Product.objects.filter()
    if request.method=="POST":
        form=AddStock(request.POST)
        if form.is_valid():
            print("form ios valid")
            name=form.cleaned_data['name']
            quant_type=form.cleaned_data['quant_type']
            quantity=form.cleaned_data['quantity']
            variety_name=form.cleaned_data['variety_name']
            price_per_unit=form.cleaned_data['price_per_unit']            
            Customer_cart_added1.objects.create(customer=cust,name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity)
            if Product.objects.filter(name=name,quant_type=quant_type):
                product=Product.objects.filter(name=name)
                qqq=product[0].total_quant+quantity
                nnn=product[0].num_varities+1
                product.update(total_quant=qqq,num_varities=nnn)
                prod_vars=Product_variety.objects.create(product=product[0],variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_added=employee)
                prod_added=Product_variety_added.objects.create(product=product[0].name,variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_added=employee)
                Product_log.objects.create(name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity,owner=cust,employee=employee,added_or_checkedout="added",price_per_unit=price_per_unit,product_net_quant=prod_vars.quantity,product_intial_quant=prod_added.quantity)
            else:
                product=Product.objects.create(name=name,total_quant=quantity,quant_type=quant_type,num_varities=1)
                prod_vars=Product_variety.objects.create(product=product,variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_added=employee)
                prod_added=Product_variety_added.objects.create(product=product.name,variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_added=employee)        
                Product_log.objects.create(name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity,owner=cust,employee=employee,added_or_checkedout="added",price_per_unit=price_per_unit,product_net_quant=prod_vars.quantity,product_intial_quant=prod_added.quantity)
            form=AddStock
            return render(request,'add_stock.html',{'form':form,'prods':prods,'cust':cust})
    return render(request,'add_stock.html',{'form':form,'prods':prods,'cust':cust})



@login_required(login_url='login')
@allowed_users(allowed_roles=['employee','admin'])
def update_customer(request,pk):
    customer=Customer.objects.filter(username=pk)
    form=Update_CustomerForm
    if request.method=="POST":
        form=Update_CustomerForm(request.POST)
        if form.is_valid():
            print("form ios valid")
            name=form.cleaned_data['name']              
            email1=form.cleaned_data['email1'] 
            address=form.cleaned_data['address']           
            customer.update(name=name,email1=email1,address=address)
            return redirect('view_stock',pk=customer[0].username)
    return render(request,'update_customer.html',{'form':form,'customer':customer[0],'cust':customer[0]})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def see_added_stocks_dates(request):
    form=DateRangeForm
    

    if request.method=="POST":
        form=DateRangeForm(request.POST)
        if form.is_valid():
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            prods=Product.objects.filter()
            check={}
            kk={}
            for i in prods:        
                prods_variety=Product_variety_added.objects.filter(created_at__range=(
                    form.cleaned_data['start_date'],
                    form.cleaned_data['end_date']
                    ),product=i.name )
                cnt=prods_variety.count()
                if cnt>10:
                    prods_variety=prods_variety[:10]
                    i.chck=1
                else:
                    i.chck=None
                if cnt>0:
                    check.update({i:prods_variety})            
            
            return render(request,'see_added_stocks_dates.html',{'check':check,'forms':forms})
    return render(request,'see_added_stocks_dates.html',{'form':form})



@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def checkout(request,pk):
    customer=Customer.objects.filter(username=pk)
    form = CheckOutStock
    message=None
    prods2=Product.objects.filter()

    if request.method=="POST":
        form=CheckOutStock(request.POST)
        if form.is_valid():
            print("form ios valid")
            name=form.cleaned_data['name']              
            variety_name=form.cleaned_data['variety_name']              
            quantity=form.cleaned_data['quantity']      
            product=Product.objects.filter(name=name)
            quant_type=product[0].quant_type 
            num_varities=product[0].num_varities     
            print(name,"TT" ,quantity,"TT",variety_name) 
            Customer_cart_checkedout1.objects.create(customer=customer[0],name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity)
            if Product_variety.objects.filter(product=product[0],variety_name=variety_name):
                prod=Product_variety.objects.filter(product=product[0],variety_name=variety_name)                
                prod5=Product_variety_added.objects.filter(product=product[0].name,variety_name=variety_name)
                price_per_unit=prod[0].price_per_unit
                cust=prod[0].owner
                employee=prod[0].employee_added
                if prod.count()>0:
                    if prod[0].quantity >= quantity:
                        if prod[0].quantity > quantity:
                            qq=prod[0].quantity-quantity
                            prod.update(quantity=qq)                                    
                            if Product_checkout.objects.filter(name=name,quant_type=quant_type):
                                product2=Product_checkout.objects.filter(name=name)
                                qqq=product2[0].total_quant+quantity
                                nnn=product2[0].num_varities+1
                                product2.update(total_quant=qqq,num_varities=nnn)                                
                                Product_variety_checkout.objects.create(Product_checkout=product2[0],variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_checkout=employee)

                            else:
                                product2=Product_checkout.objects.create(name=name,total_quant=quantity,quant_type=quant_type,num_varities=1)
                                Product_variety_checkout.objects.create(Product_checkout=product2,variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_checkout=employee)                        
                            
                            print(prod[0],prod[0].quantity)
                            print("quantity reduced")
                            Product_log.objects.create(name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity,owner=customer[0],employee=employee,added_or_checkedout="checkedout",price_per_unit=price_per_unit,product_intial_quant=prod5[0].quantity ,product_net_quant=prod[0].quantity)
                            
                            return redirect('view_stock',pk=customer[0].username)
    
                        else:
                            if Product_checkout.objects.filter(name=name,quant_type=quant_type):
                                product2=Product_checkout.objects.filter(name=name)
                                qqq=product2[0].total_quant+quantity
                                nnn=product2[0].num_varities+1
                                product2.update(total_quant=qqq,num_varities=nnn)                                
                                Product_variety_checkout.objects.create(Product_checkout=product2[0],variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_checkout=employee)
                            else:
                                product2=Product_checkout.objects.create(name=name,total_quant=quantity,quant_type=quant_type,num_varities=1)
                                Product_variety_checkout.objects.create(Product_checkout=product2,variety_name=variety_name,quantity=quantity,price_per_unit=price_per_unit,owner=cust,employee_checkout=employee)                        
                            
                            product.update(name=name,num_varities=num_varities-1)
                            product[0].save()
                            print("instance deleted")
                            Product_log.objects.create(name=name,variety_name=variety_name,quant_type=quant_type,quantity=quantity,owner=customer[0],employee=employee,added_or_checkedout="checkedout",price_per_unit=price_per_unit,product_intial_quant=prod5[0].quantity ,product_net_quant=prod[0].quantity)
                            prod[0].delete()
                            return redirect('view_stock',pk=customer[0].username)
                    else:
                        message="Available Quantity is less than entered quantity !!"
            else:
                message="Product not found, check details !!"
    return render(request,'checkout.html',{'form':form,'message':message,'prods2':prods2,'cust':customer[0]})     



@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def prod_varities(request,pk):
    pp=Product.objects.filter(product_uid=pk)
    prods=Product_variety.objects.filter(product=pp[0])
    return render(request,'prod_varities.html',{'prods':prods,'pp':pp})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def see_stocks(request):
    prods=Product.objects.filter()
    check={}
    kk={}
    for i in prods:        
        prods_variety=Product_variety.objects.filter(product=i)
        cnt=prods_variety.count()
        if cnt>10:
            prods_variety=prods_variety[:10]
            i.chck=1
        else:
            i.chck=None
        check.update({i:prods_variety})

    return render(request,'see_stocks.html',{'check':check})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def prod_varities_admin(request,pk):
    pp=Product.objects.filter(product_uid=pk)
    prods=Product_variety.objects.filter(product=pp[0])
    labels=[]
    data=[]
    for i in prods:
        labels.append(i.variety_name)
        data.append(i.quantity)
    return render(request,'prod_varities_admin.html',{'prods':prods,'pp':pp,'data':data,'labels':labels})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def see_stocks_admin(request):
    form=SearchForm
    if request.method=="POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            product_name=form.cleaned_data['product_name']
            min_quantity=form.cleaned_data['min_quantity']
            prods=Product.objects.filter(name=product_name)
            if prods:
                check={}
                kk={}
                for i in prods:        
                    prods_variety=Product_variety.objects.filter(product=i,quantity__gte=min_quantity)
                    cnt=prods_variety.count()
                    if cnt>10:
                        prods_variety=prods_variety[:10]
                        i.chck=1
                    else:
                        i.chck=None
                    check.update({i:prods_variety})
                return render(request,'see_stocks_admin.html',{'check':check})
            else: #No product exists
                messages.error="Not Available"
                return render(request,'see_stocks_admin.html',{'messages':messages})
    prods=Product.objects.filter()
    check={}
    labels=[]
    data=[]
    for i in prods:
        labels.append(i.name)
        data.append(i.total_quant)
        prods_variety=Product_variety.objects.filter(product=i)
        
        cnt=prods_variety.count()
        if cnt>10:
            prods_variety=prods_variety[:10]
            i.chck=1
        else:
            i.chck=None
        check.update({i:prods_variety})
    return render(request,'see_stocks_admin.html',{'check':check,'form':form,'labels': labels,'data': data})


@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def prod_out_varities(request,pk):
    pp=Product_checkout.objects.filter(product_uid=pk)
    prods=Product_variety_checkout.objects.filter(Product_checkout=pp[0])
    return render(request,'prod_out_varities.html',{'prods':prods,'pp':pp})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def see_out_stocks(request):
    prods=Product_checkout.objects.filter()
    check={}
    kk={}
    for i in prods:        
        prods_variety=Product_variety_checkout.objects.filter(Product_checkout=i)
        cnt=prods_variety.count()
        if cnt>10:
            prods_variety=prods_variety[:10]
            i.chck=1
        else:
            i.chck=None
        check.update({i:prods_variety})

    return render(request,'see_out_stocks.html',{'check':check})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def prod_out_varities_admin(request,pk):
    pp=Product_checkout.objects.filter(product_uid=pk)
    prods=Product_variety_checkout.objects.filter(Product_checkout=pp[0])
    return render(request,'prod_out_varities_admin.html',{'prods':prods,'pp':pp})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def see_out_stocks_admin(request):
    form=DateRangeForm    
    if request.method=="POST":
        form=DateRangeForm(request.POST)
        if form.is_valid():
            labels=[]
            data=[]
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            prods=Product_checkout.objects.filter()
            check={}
            kk={}
            for i in prods:        
                prods_variety=Product_variety_checkout.objects.filter(Product_checkout=i)
                labels.append(i.name)
                data.append(i.total_quant)
                cnt=prods_variety.count()
                if cnt>10:
                    prods_variety=prods_variety[:10]
                    i.chck=1
                else:
                    i.chck=None
                check.update({i:prods_variety})

            return render(request,'see_out_stocks_admin.html',{'check':check,'labels':labels,'data':data})
    return render(request,'see_out_stocks_admin.html',{'form':form})







def GeneratePDF( request,pk):
    cust=Customer.objects.get(username=pk)
    cart=Customer_cart_added1.objects.filter(customer=cust)
    template = get_template('invoice.html')
    context = {
        "invoice_id": 123,
        "customer_name": cust.name,
        "customer_username": cust.username,
        
        "today": datetime.datetime.now(),
        "employee":cust.employee.name,
        "prods":cart
    }
    
    pdf = render_to_pdf('pdf/invoice.html', context)
    cart.delete()
    return HttpResponse(pdf, content_type='application/pdf')


def GeneratePDF2( request,pk):
    cust=Customer.objects.get(username=pk)
    cart=Customer_cart_checkedout1.objects.filter(customer=cust)
    template = get_template('invoice2.html')
    context = {
        "invoice_id": 123,
        "customer_name": cust.name,
        "customer_username": cust.username,
        
        "today": datetime.datetime.now(),
        "employee":cust.employee.name,
        "prods":cart
    }
    
    pdf = render_to_pdf('invoice2.html', context)
    cart.delete()
    return HttpResponse(pdf, content_type='application/pdf')





def GeneratePDF3( request,pk):
    cust=Customer.objects.get(username=pk)
    cart=Product_variety.objects.filter(owner=cust)
    print(cart)
    template = get_template('invoice3.html')
    context = {
        "invoice_id": 123,
        "customer_name": cust.name,
        "customer_username": cust.username,        
        "today": datetime.datetime.now(),
        "employee":cust.employee.name,
        "prods":cart
    }
    
    pdf = render_to_pdf('invoice3.html', context)
    
    return HttpResponse(pdf, content_type='application/pdf')


def testing_css(request):
    return render(request,'testing_css.html',{})