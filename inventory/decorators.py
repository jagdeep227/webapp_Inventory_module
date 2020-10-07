from django.http import HttpResponse
from django.shortcuts import redirect,render
from .models import *

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('base')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group,"###############")
            if group in allowed_roles:
                print("Going to base only")
                return view_func(request, *args, **kwargs)
            if request.user.is_superuser:
                print("Going to base only")
                return view_func(request, *args, **kwargs)
            else:
                print(group+'/'+str(request.user.id),"%%%%%%%%%%%%%%%%%%%")
                roles1=['employee']
                if group in roles1:
                    print("Going to base employee")                    
                    return render(request,'base_employee.html',{})
                roles2=['customer']
                if group in roles2:
                    cust=Customer.objects.filter(user=request.user)
                    print("Going to Customer")                    
                    return render(request,'customer.html',{'cust':cust[0]})
        return wrapper_func
    return decorator

