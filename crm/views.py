from django.shortcuts import render,redirect
from crm.forms import EmployeeModelForm,Registrationform,Loginform
from django.views.generic import View
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_requried(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
@method_decorator(signin_requried,name="dispatch")
class EmployeecreateView(View):
   
    def get(self,request,*args,**kwargs):
        form=EmployeeModelForm()
        return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"employee has been added")
            # Employees.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"failed to add employee!!")
            return render(request,"emp_add.html",{"form":form})
        

@method_decorator(signin_requried,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
       qs=Employees.objects.all()
       departments=Employees.objects.all().values_list("department",flat=True).distinct()
       print(departments)
       if "department" in request.GET:
           dept=request.GET.get("department")
           qs=qs.filter(department__iexact=dept)
       return render(request,"emp_list.html",{"data":qs,"departments":departments})
        

    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})

@method_decorator(signin_requried,name="dispatch")
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_detail.html",{"data":qs})
@method_decorator(signin_requried,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"deleted successfully!!")
        return redirect("emp-all")
@method_decorator(signin_requried,name="dispatch")
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       obj=Employees.objects.get(id=id)
       form=EmployeeModelForm(instance=obj)
       return render(request,"emp_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"change employee successfully!!")
          
            return redirect("emp-detail",pk=id)
        else:
            messages.error(request,"failed to change employee")
            return render(request,"emp_edit.html",{"form":form})

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=Registrationform()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=Registrationform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            # form.save()
            messages.success(request,"created")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed")
            return render(request,"register.html",{"form":form})
        

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=Loginform()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid credential")
                login(request,user_obj)
                return redirect("emp-all")
            
        messages.error(request,"invalid credential")
        return render(request,"login.html",{"form":form})
@method_decorator(signin_requried,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

