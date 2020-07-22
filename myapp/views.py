from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,reverse
from . models import *
from django.core.mail import send_mail
from django.utils.html import strip_tags
from . import utils
import random
from django.forms import ModelForm
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


# Create your views here.
def IndexPage(request):
    if request.session.get('id'):
        try:
            EmailId=request.session.get('email')
            print("EmailId===================",EmailId)
            
            u=Usertb1.objects.get(pk=request.session.get('id')) #SELECT * from Usertb1 WHERE pk=id  #It will return object
            print("u=======================",u)

            UserName=request.session.get('uname')
            print("Username=====================",UserName)
                    
        except:
            #del request.session['id']
            print("del=======================")
            return HttpResponseRedirect(reverse('loginpage'))
        
        return render(request,'myapp/index.html')
    else:
        return HttpResponseRedirect(reverse('loginpage'))

def BlogPage(request):
    return render(request,'myapp/blog.html')

def CategoryPage(request):
    return render(request,'myapp/category.html')


def CartPage(request):
    return render(request,'myapp/cart.html')

def ContactPage(request):
    return render(request,'myapp/contact.html')

def RegisterPage(request):
    if request.method=="POST":
        exid=request.POST.get('ext_id')
        uname=request.POST.get('username')
        eid=request.POST.get('emailid')
        pwd=request.POST.get('password')
        cpwd=request.POST.get('cpassword')
        otp=str(random.randint(0000,9999))
        u_list=Customertbl.objects.filter(UserName=uname)
        if u_list:
            message="User is already available"
            return render(request,'myapp/register.html',{'msg':message})
        e_list=Customertbl.objects.filter(EmailId=eid)
        if e_list:
            message="Email id is already available"
            return render(request,'myapp/register.html',{'msg':message})
        if pwd==cpwd:
            user=Customertbl.objects.create(UserName=uname,EmailId=eid,Password=pwd,Otp_num=otp,Extra_Id=exid)
            utils.OtpFun(user)
            print("=================Email Send Sucessfully==================")
        else:
            msg="Password and confirm password are not matched!"
            return render(request,'myapp/register.html',{'msg':message})
    return render(request,'myapp/register.html')

def OtpPage(request):
        exid=request.POST.get('id')
        obj=Customertbl.objects.filter(pk=exid)
        otp=request.POST.get('otp_text')
        if obj:
            if otp==(obj[0].Otp_num):
                obj[0].is_varified=True
                obj[0].save()
                request.session['id']=obj[0].pk
                return HttpResponseRedirect(reverse('indexpage'))
            else:
                message="Otp is wrong!!!!!!!"
                print("login=====================")
                return render(request,'myapp/login.html',{'msg':message,'user':obj[0]})
def LoginPage(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        checked=Customertbl.objects.filter(UserName=uname,Password=pwd)
        print("Checked======================",checked)
        if checked:
            if checked[0].is_varified:
                request.session['id']=checked[0].pk
                request.session['email']=checked[0].EmailId
                return HttpResponseRedirect(reverse('indexpage'))
            else:
                print("Inside else========================")
                return render(request,'myapp/otp.html',{'user':checked[0]})

        message="Username or password are incorrect"
        return render(request,'myapp/login.html',{'msg':message})

    return render(request,'myapp/login.html')