#for email
from email import message
import email
from django.core.mail import send_mail,BadHeaderError
# end email
import re
from statistics import quantiles
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from requests import session
from urllib3 import Retry
from .forms import SingUpForm
from django.core.paginator import Paginator
from .models import Contact, Item,Cart,Order,OrderItem,OrderDetail
from ecom import settings
from django.db.models import Q


#for pyment methood 
import stripe
from django.http.response import HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def index(request):
    all_data = Item.objects.all()
    if request.method =="POST":
        s1= request.POST.get('search1')
        s2=all_data
        if s2.filter()== s1:
            print("same")
        return redirect("/index/")
    
    return render(request,"index.html")

def user_login(request):
    if request.method == "POST":
        print("loggin")
        fm =AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            print(uname)
            print(upass)
            user = authenticate(username =uname,password =upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/index')

    else:
        fm = AuthenticationForm()
    return render(request,"login.html",{'form':fm})


def singup(request):
    if request.method == "POST":
        print()
        fm = SingUpForm(request.POST)
        if fm.is_valid():
            fm.save() 

    # welcome email
        print("emial")
        user =request.user
        subject = 'welcome to GFG world'
        message = f'Hi {user.username}, thank you for registering in Ecommeere.'
        email_from = settings.EMAIL_HOST_USER
        if request.method == 'POST':
            em = request.POST.get('email')
            print("---------->email",em)
            recipient_list = [em]
            send_mail( subject, message, email_from, [recipient_list]) 
        return redirect("/login/")  
    else:
        fm= SingUpForm()
    return render(request,'singup.html',{"form":fm})

def user_logout(request):
    logout(request)
    return redirect('/index/')

def change_password(request):
    fm = PasswordChangeForm(user=request.user)
    return render(request,"forget_password.html",{"form":fm})

def products(request):
    print("hello1")   
    all_data = Item.objects.all()
    paginator = Paginator(all_data,6)
    page_number = request.GET.get('page')
    page_obj  =paginator.get_page(page_number)  
    if request.method == "POST":
        print("hello---------->>>pravin")
        name = request.POST.get("search1")
        print(name)
        s = str(Item.item_name)
        print(all_data.filter(item_name= "tv"))
        print("---->",s)
    return render(request,"products.html",{"page_obj":page_obj})

def about(request):
    return render(request,"about.html")

def contact(request):
    all_contact = Contact.objects.all()
    if request.method =="POST":
        name= request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        obj = Contact(name=name,email=email,subject=subject,message=message)
        obj.save()
    return render(request,"contact.html")

def add_product(request):

    return render(request,"add_product.html")

def info(request,pk):
    page_obj = Item.objects.get(id=pk)

    return render(request,"info.html",{"page_obj":page_obj})

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        print("---***************",user)
        cart = Cart.objects.filter(user=user)  
        all_price=0
        print("----------hello",cart)
        for i in cart:
            print('item-------------->item',i.total_item)
           
            price =i.total_item*i.totalamount
            print("one item price---->", price)
            all_price+=i.totalamount
        total = Cart.objects.all()
        print("--------------------------------------------->",total)
    
        return render(request,"cart.html",{"all_cart":cart,'all_price':all_price,'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})

def addtocart(request):
    if request.user.is_authenticated:
        print("hello2--------->")
        user = request.user
        print("user-->",user)
        product_id= request.GET.get('prod_id') 
        print("product_id->",product_id)
        product = Item.objects.get(id=product_id)
        print('------------>product',product)
        print("product->", product.price)

        Cart(user = user, item=product, totalamount=product.price).save()
        messages.success(request, ' Add product Successfully!')
        return redirect("/products")
    else:
        return redirect("/login")

def removecart(request):
    print("--->remove")
    
    if request.method == "GET":
        product_id= request.GET.get('prod_id') 
        print("product_id->",product_id)
        product = Cart.objects.filter(Q(item = product_id)& Q(user = request.user))
        print("remove product->",product)
        product.delete()
        messages.success(request, ' Remove Product Successfully!')
        return redirect("/cart")
    # return render(request,"cart.html")


    
def pluscart(request, id):
    print("pluse")
    if request.method == "GET":
        plu= Cart.objects.filter(id=id).filter(user=request.user).first()
        print(plu)
        plu.total_item+=1 
        print("itme_price---->",plu.item.price)
        print("total_item",plu.total_item)
        print("itme_name------>",plu.item.item_name)
        price= plu.item.price
        item = plu.total_item
        print('price------>',price)
        print('item------>',item)
        all = item*price
        print("all-=---------->",all)
        plu.totalamount=all
        # print()
        plu.save()
        # plu.save()
        price =0.0    
        shipping_amount = 0.0
        cart_item = [i for i in Cart.objects.all() if i.user == request.user ]
        for i in cart_item:
            tempamoutn = (i.total_item * i.item.price)
            price+=tempamoutn
            print('------------->price',price)
        data ={
            'total_item':plu.total_item,
            'price':price,
            'totalamount':price
        }
        return redirect('cart')

def minuscart(request, id):
    if request.method == "GET":
        plu= Cart.objects.filter(id=id).filter(user=request.user).first()
        print(plu)
        plu.total_item-=1 
        print("itme_price---->",plu.item.price)
        print("total_item",plu.total_item)
        print("itme_name------>",plu.item.item_name)
        price= plu.item.price
        item = plu.total_item
        print('price------>',price)
        print('item------>',item)
        all = item*price
        print("all-=---------->",all)
        plu.totalamount=all
        plu.save()
        price =0.0    
        shipping_amount = 0.0
        cart_item = [i for i in Cart.objects.all() if i.user == request.user ]
        for i in cart_item:
            tempamoutn = (i.total_item * i.item.price)
            price+=tempamoutn
            print('------------->price',price)
        data ={
            'total_item':plu.total_item,
            'price':price,
            'totalamount':price
        }
        return redirect('cart')


def search(request):
    print("hello")
    return render(request,"index.html")

def order(request):
    
    return render(request,"oder.html")

def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    price = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_item = [i for i in Cart.objects.all() if i.user == request.user ]
    if cart_item:
        for i in cart_item:
            tempamoutn = (i.total_item * i.item.price)
            price+=tempamoutn
            totalamount = price+shipping_amount
    return render(request,"checkout.html",{"totalamount":totalamount,"cart":cart})



@csrf_exempt
def create_checkout_session(request, id):
    print(type(id))
    request_data = request.user.email
    user = request.user
    cart = Cart.objects.filter(user=user)
    if type(id) == str:
        all_price=0
        for i in cart:
            all_price+=i.totalamount
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            customer_email = "abc@gmail.com",
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                        'name': "All Products",
                        },
                        'unit_amount': all_price *100,  
                    },
                    'quantity': 1,
                }
            ],
            
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )
        order = OrderDetail()
        order.customer_email = "abc@gmail.com"
        order.stripe_payment_intent = checkout_session['payment_intent']
        order.amount = int(all_price * 100)
        order.save()
        return JsonResponse({'sessionId': checkout_session.id})

def success(request):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
    return render(request,'success.html')

def failed(request):
    
    return render(request,"failed.html")
