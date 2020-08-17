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
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .paytm import generate_checksum,verify_checksum
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def IndexPage(request):
    if request.session.get('id'):
        try:
            #EmailId=request.session.get('email')
            #print("EmailId===================",EmailId)
            
            u=Customertbl.objects.get(pk=request.session.get('id')) #SELECT * from Usertb1 WHERE pk=id  #It will return object
            print("u=======================",u)
            #p=Producttbl.objects.get(pk=request.session.get('id'))
            #print("p========================",p)
            #UserName=request.session.get('uname')
            #print("Username=====================",UserName)
                    
        except:
            #del request.session['id']
            #print("del=======================")
            return HttpResponseRedirect(reverse('loginpage'))
        users = Producttbl.objects.all()

        for user in users:
            print("\n Product:",user)
            print("\n Name:",user.ProductName)
            print("\n Price:",user.ProductPrice)
        print("outside index=============================")
        return render(request,'myapp/index.html',{'all_user':users})
    else:
        return HttpResponseRedirect(reverse('loginpage'))

def BlogPage(request):
    return render(request,'myapp/blog.html')

def CategoryPage(request):
    if request.session.get('id'):
        #try:
            #p=Producttbl.objects.get(pk=request.session.get('id'))
            #print("p========================",p) 
        #except:
            #del request.session['id']
            #print("del=======================")
            #return HttpResponseRedirect(reverse('categorypage'))
        users = Producttbl.objects.all()
        for user in users:
            print("\n Product:",user)
            print("\n Name:",user.ProductName)
            print("\n Price:",user.ProductPrice)
        print("outside index=============================")
        return render(request,'myapp/category.html',{'all_user':users})
    else:
        return HttpResponseRedirect(reverse('categorypage'))

    return render(request,'myapp/category.html')


def CartPage(request):  ### product object,customer object,price
    
        cus=Customertbl.objects.get(pk=request.session.get('id')) ### Customer object
        if request.method=="POST":
            pro_id=request.POST.get('product_id')
            print("pro_id=============",pro_id)
            pro=Producttbl.objects.get(id=pro_id)   ### product object
            print("Product Object=======",pro)
            pro_available=Carttbl.objects.filter(product_id=pro,user_to_id=cus)
            if pro_available:
                pro_available[0].Quantity += 1
                pro_available[0].Total_price=pro.ProductPrice * pro_available[0].Quantity
                pro_available[0].save()
                cart_value=Carttbl.objects.filter(user_to_id=cus) ### login user
                print("cart_value==================",cart_value)
                return render(request,'myapp/cart.html',{'all_product':cart_value})
                #return render(request,'myapp/cart.html')
            #cus=Customertbl.objects.get(pk=request.session.get('id')) ### Customer object
            #print("Customer Object==========",cus)
            price=pro.ProductPrice ###product price
            #order=Carttbl.objects.create(user_to_id=cus,product_id=pro,Total_price=price)
            if pro_id:
                order=Carttbl.objects.create(user_to_id=cus,product_id=pro,Total_price=price)
                #order.Quantity += 1
                #print("=================Temp=========",order.Quantity)
                #order.save()

        cart_value=Carttbl.objects.filter(user_to_id=cus) ### login user
        print("cart_value==================",cart_value)
         
        #check if the order item is in the cart
        #if cart_value.exists():
            #order.Quantity += 1
            #order.save()
        #else:
            #Carttbl.objects.create(user_to_id=cus,product_id=pro,Total_price=price)
            #print("Cart value added==============================")

        return render(request,'myapp/cart.html',{'all_product':cart_value})
        

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

def QuantityhandlePage(request):
    #print("\n\n\n\n\n\nrequest===============",request)
    cart_obj=Carttbl.objects.get(id=request.GET.get('cart_id')) #cart object getting from html page
    print("===========\n\n\n\ncart_obj============",cart_obj)
    if request.GET.get('minus'):
        #print("===========temp============",cart_obj.Quantity)
        cart_obj.Quantity -= 1
        #print("\n\n\n\nQuantity minus==============",cart_obj.Quantity)
        
    if request.GET.get('plus'):
        #print("\n\n\n\n============price==============",cart_obj.Total_price)
        #print("===========temp============",cart_obj.Quantity)
        cart_obj.Quantity += 1

    cart_obj.Total_price = cart_obj.Quantity * cart_obj.product_id.ProductPrice
    cart_obj.save()
    return HttpResponseRedirect(reverse('cartpage')) 

def MinusFunction(request):
    print("\n\n\n==========minus function===================")
    print("request=================",request)
    cart_obj=Carttbl.objects.get(id=request.GET.get('quant_id')) #cart object getting from html page
    print("===========\n\n\n\ncart_obj============",cart_obj)
    cart_obj.Quantity -= 1
    cart_obj.Total_price = cart_obj.Quantity * cart_obj.product_id.ProductPrice
    cart_obj.save()
    print({'qunatity':cart_obj.Quantity,'total_price':cart_obj.Total_price,'quantity_id':"quantity%d"%(cart_obj.id)})
    return JsonResponse({'qunatity':cart_obj.Quantity,'total_price':cart_obj.Total_price,'quantity_id':"quantity%d"%(cart_obj.id),'price':"#price_id%d"%(cart_obj.id)})
        
def PlusFunction(request):
    pass
               

def PayPage(request):
    if request.method == "GET":
        return render(request, 'myapp/pay.html')
    try:
        cus=Customertbl.objects.get(pk=request.session.get('id'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        amount = int(request.POST['amount'])
        user = Customertbl(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'myapp/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transactiontbl.objects.create(made_by=user, amount=20000)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'myapp/redirect.html', context=paytm_params)

@csrf_exempt
def CallbackPage(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'myapp/callback.html', context=received_data)

      
