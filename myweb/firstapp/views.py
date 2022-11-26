from time import sleep
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from firstapp.models import *
from secondapp.models import *
from django.db.models import Q
import array as arr
from ast import literal_eval 
import random
import string
import json
import requests

# Create your views here.

@never_cache
def index1(request):
    if request.user.is_authenticated:
        return redirect("/home")
    if request.COOKIES.get('list_item'):
        length = literal_eval(request.COOKIES.get('list_item'))
        value = len(length)
    else:
        value = 0       
    category = add_category.objects.filter()
    pr = add_product.objects.filter().order_by('?')[:8]
    offers = offer.objects.filter()
    cat_offer = offer.objects.filter().order_by('?')[:2]
    return render(request, 'site/landing.html',{'category_list':category , 'pr':pr , 'offers':offers , 'cat_offer':cat_offer , 'value':value})
    
@never_cache
def home(request):
    if request.user.is_authenticated and request.user.is_active: 
        category = add_category.objects.filter()
        c = cart.objects.filter( user_name_id = request.user.id).count()
        pr = add_product.objects.filter().order_by('?')[:8]
        offers = offer.objects.filter()
        cat_offer = offer.objects.filter().order_by('?')[:2]
        return render(request, 'site/index.html',{'category_list':category , 'cart_count':c , 'pr':pr , 'offers':offers , 'cat_offer':cat_offer})
    else:
         return redirect("/login")

def user_signup(request):
    if request.user.is_authenticated:
        return redirect("/home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone_no')
        if username  and password and phone:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is already exists')
                return redirect('/signup')
            else:
                # details = User(username=username,password=password, phone=phone)
                # details.save()
                generat_otp()

                return render(request, 'site/otp.html')
        else:
            messages.error(request , 'All fields are required')
            return redirect('/signup')
    return render(request, 'site/signup.html')


def validate(request):
    
    if request.method == "POST":
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        list=[otp1,otp2,otp3,otp4]
        try:
            s=[str(i) for i in list]
            res = int("".join(s))
            print(res) 
            print(generated_otp)
            if res == generated_otp:
                return render(request, 'site/signup3.html')
            else:
                messages.error(request,'Invalid OTP')
                return redirect('validate')
          
        except: 
            messages.error(request, 'Enter Your OTP')
            return redirect('validate')
    return render(request,'site/otp.html')       

def user_details(request):
    if request.method =="POST":
        username1 = request.POST.get('username')
        password2 = request.POST.get('password')
        phone = request.POST.get('phone_no')
        email = request.POST.get('email')
        referal = request.POST.get('referal')
        print(username1 , password2 , phone , email)

        if referal:
           if User.objects.filter(referal_id = referal).exists():
               finded_user = User.objects.filter(referal_id = referal)
               for i in finded_user:
                   total_wallet = i.wallet_amount
                   total_wallet = total_wallet + 100
                   i.wallet_amount = total_wallet
                   i.save()
           else:
               messages.error(request , 'Invalid Referal Code')  
               return redirect('/save')  
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        use = User.objects.create_user(username=username1,password=password2, email=email, phone=phone , referal_id = result_str , wallet_amount = 100) 
       
        login(request,use)
        gest_user_cart(request)
        return redirect('/home')
    return render(request,'signup3.html')   
           
            

def user_login(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('/home')
    if request.method == "POST":
        username1 = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username1,  password=password)
        try:
           chek = User.objects.get(username=username1)
        except:
            messages.error(request, 'Account not found')
            return redirect('/login')
        if chek.is_active == True:
            if user is not None :
                login(request, user)
                gest_user_cart(request)
                variable = redirect('/home')
                variable.delete_cookie('list_item')
                variable.delete_cookie('detail')
                return variable
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('/login')
        else:
            messages.error(request, 'Account Blocked')
            return redirect('/login')
    return render(request, 'site/user_login.html')



def gest_user_cart(request):
   if request.COOKIES.get('detail'):
        datas = literal_eval(request.COOKIES.get('detail'))
        it =  cart.objects.filter(user_name = request.user.id)
        for na in datas:
            pr_names = na['pr_name']
            print(pr_names)
            fin_pr = add_product.objects.get(product_name = pr_names)
            if it:
                for i in it:
                    if not cart.objects.filter(user_name = request.user.id , prd_name = fin_pr).exists():
                        
                        print("delete dup")
                        print(fin_pr)
                        print("in")
                        fin_pr = add_product.objects.get(product_name = fin_pr)
                        sa_c = cart()
                        sa_c.prd_name = fin_pr
                        sa_c.total_amount = int(na['total_amount'])
                        if fin_pr.offer_reduced_price:
                            sa_c.ofer_reduced_price = fin_pr.offer_reduced_price
                        else:
                            sa_c.ofer_reduced_price =  None
                        sa_c.user_name = User.objects.get(id=request.user.id)
                        sa_c.quantity = int(na['quantity'])
                        sa_c.save()
                                      
            else:   
                
                sa_c = cart()
                sa_c.prd_name = fin_pr
                sa_c.user_name = User.objects.get(id=request.user.id)
                sa_c.quantity = int(na['quantity'])
                sa_c.total_amount = int(na['total_amount'])
                if fin_pr.offer_reduced_price:
                    sa_c.ofer_reduced_price = fin_pr.offer_reduced_price
                else:
                    sa_c.ofer_reduced_price =  None
                sa_c.user_name = User.objects.get(id=request.user.id)
                sa_c.save()
                    


def login_otp(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        if mobile_no is None:
            messages.error(request , 'Enter Your Mobile Number')
            return redirect('/login_otp')
        print(mobile_no)
        if User.objects.filter(phone = mobile_no).exists():
            generat_otp()
            messages.success(request,'OTP genereted Sucessfuly')
            information = User.objects.get(phone=mobile_no)
            return render(request,'site/login_render_for_otp.html',{'info':information})
        else:    
            messages.error(request,'Phone number is not exists ')
            return redirect('/login_otp')
            
    return render(request,'site/login_otp.html')

def render_login_page(request,da):
    if request.method == 'POST':
        try:
           login_otp = int(request.POST.get('login_otp'))
        except:
            messages.error(request , 'Enter OTP')
            return redirect('/login_otp')
       
        if login_otp == generated_otp:
            user = User.objects.get(id=da)
            login(request,user)
            return redirect('/home')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('/login_otp')
        

def user_profile_edit(request):
    if request.method == 'POST':
        details = User.objects.get(id = request.user.id)
        details.username = request.POST.get('name')
        details.phone = request.POST.get('number')
        details.email = request.POST.get('email')
        details.save()
        return redirect('/userprofile')

def edit_address(request):
    try:
        information = address.objects.get(user_id_id = request.user.id)
        if request.method == 'POST':
            edit = address.objects.get(user_id_id = request.user.id)
            edit.name = request.POST.get('first-name')
            edit.email = request.POST.get('email')
            edit.phone_no = request.POST.get('phone')
            edit.country = request.POST.get('select')
            edit.state = request.POST.get('state')
            edit.city = request.POST.get('city')
            edit.pincode = request.POST.get('pin')
            edit.address = request.POST.get('address')
            edit.save()
            messages.success(request, ' Address edited sucessfully')
            return redirect('/edit_address')  
        return render(request, 'site/edit_address.html' , {'info':information})
    except:
            messages.success(request, 'You have NO address Please Add address')
            return redirect('/userprofile')

def user_logout(request):
    logout(request)
    return redirect('/')

def user_profile(request):
    user = User.objects.get(id = request.user.id)
    user_address = address.objects.filter(user_id = request.user.id)
    return render(request,'site/userprofile.html',{'details':user , 'user_address':user_address})

def shoping(request,ca):
    t = None
    c = cart.objects.filter( user_name_id = request.user.id).count()
    try:
        cate = add_category.objects.get(slug = ca)
        prd = add_product.objects.filter(category_name_id = cate.id)
        page  = Paginator(prd , 2)
        page_no = request.GET.get('page')
        use_page = page.get_page(page_no)
        
    except:
        use_page = None   
    price = request.GET.get('m_price' , '')     
    if price:
        max_price = int(price.split(",",1)[0])
        min_price = int(price.split(",",1)[1])
        item = add_product.objects.filter(original_price__lte = max_price , original_price__gte = min_price)
        use_page = item
        t = 1
    return render(request, 'site/shop.html',{ 'show':use_page , 't':t , 'cart_count':c})

@never_cache
def pr_detail(request,nu,n):
    product_details = add_product.objects.get(slug=nu)
    list_prd = add_product.objects.filter( category_name_id = n)
    check = cart.objects.filter(user_name = request.user.id) 
    c = cart.objects.filter( user_name_id = request.user.id).count()
    name_pr = None
    for i in check:
        if i.prd_name_id == product_details.id:
            name_pr = i.prd_name
            break
        else:
            name_pr = None
    return render(request, 'site/detail.html',{'pr_details':product_details, 'list':list_prd , 'check':name_pr, 'cart_count':c })
   
def getqantity(request):
    c = request.GET.get('cat_name')
    r = request.GET.get('prd_id')
    ta = request.GET.get('totalamount')
    pr = add_product.objects.get(id=r)
    sum = 0
    va = int(c)
   
    cooki_list = []
        
    if request.COOKIES.get('detail'):
        d = literal_eval(request.COOKIES.get('detail'))
        for i in d:
            cooki_list.append(i) 
    
        if va >= pr.stock:
            for t in cooki_list:
                total = int(t['total_amount'])
                sum = sum + total
            return JsonResponse({'msg':"limited stock" , 'qu':sum})    
        for di in cooki_list:
            if di['pr_name'] == pr.product_name:
                print("in change")
                di['quantity'] = c
                di['total_amount'] = ta
                length = literal_eval(request.COOKIES.get('list_item'))
                if len(length) == 1:
                    finded = add_product.objects.get(id = r)
                    if finded.selling_price:
                        price = finded.selling_price
                    else:
                        price = finded.original_price    
                    
                    sum = price + int(ta)
                   
                else:    
                    for t in cooki_list:
                        total = int(t['total_amount'])
                        sum = sum + total
                se = JsonResponse({'qu':sum})
                se.set_cookie('detail' , cooki_list)
                return se
          
    else:    
 
        cart_p = cart.objects.filter(user_name_id = request.user.id)
        for s in cart_p :  
            if s.prd_name == pr:
                s.quantity = c
                s.total_amount = ta
                cart_quantity = s.quantity
                s.save()
            su = int(s.total_amount)
            sum = sum + su 
        a = int(cart_quantity)
        b = int(pr.stock)
        if a >= b:
            return JsonResponse({'msg':"limited stock" , 'qu':sum})
     
    return JsonResponse({'qu':sum})



def cart1(request):
    if request.user.is_authenticated:
        c = request.GET.get('val')
        it =  cart.objects.filter(user_name = request.user.id)
        fin_pr = add_product.objects.get(id=c)
        if it:
            for i in it:
                if i.prd_name == fin_pr:
                    return JsonResponse({"mess": 'Item is already in cart'})
                         
            find_pr = add_product.objects.get(id=c)
            sa_c = cart()
            sa_c.prd_name = find_pr
            if fin_pr.selling_price :
                sa_c.total_amount = int(find_pr.selling_price)
                sa_c.ofer_reduced_price = fin_pr.offer_reduced_price
            else:
                sa_c.total_amount = int(find_pr.original_price)
            current_user = request.user
            sa_c.user_name = User.objects.get(id=current_user.id)
            sa_c.save()
    
            return JsonResponse({'mess':"iteam added to your cart"})    
        else:   
               
                find_pr = add_product.objects.get(id=c)
                sa_c = cart()
                sa_c.prd_name = find_pr
                if fin_pr.selling_price :
                    sa_c.total_amount = int(find_pr.selling_price)
                    sa_c.ofer_reduced_price = fin_pr.offer_reduced_price    
                else:
                    sa_c.total_amount = int(find_pr.original_price)
                current_user = request.user
                sa_c.user_name = User.objects.get(id=current_user.id)
                sa_c.save()
        
                return JsonResponse({'mess':"iteam added to your cart"})        

    else:
        list_pr = []
        cook_list = []
        if request.COOKIES.get('list_item') :
            last = literal_eval(request.COOKIES.get('list_item'))
            data_list = literal_eval(request.COOKIES.get('detail'))
            for d in data_list:
                cook_list.append(d)
            for i in last:
                list_pr.append(i)  
            val = request.GET.get('val')
            fin_product = add_product.objects.get(id=val)
            if fin_product.selling_price:
                price = fin_product.selling_price
            else:
                price = fin_product.original_price    
            for i in last:
                if i != fin_product.product_name:
                    list_pr.append(fin_product.product_name)   
                    res = JsonResponse({'mess':"iteam added to your cart"})  
                    dic = {
                    'quantity':1,
                    'total_amount':price,
                    'pr_name':fin_product.product_name
                    }
                    cook_list.append(dic)
                    res.set_cookie('list_item' , list_pr) 
                    res.set_cookie('detail' , cook_list) 
                    return res
                return JsonResponse({"mess": 'Item is already in cart'})    
        else:
            val = request.GET.get('val')
            fin_product = add_product.objects.get(id=val)
            if fin_product.selling_price:
                price = fin_product.selling_price
            else:
                price = fin_product.original_price  
            dic = {
                'quantity':1,
                'total_amount':price,
                'pr_name':fin_product.product_name
            }    
            n = fin_product.product_name
            cook_list.append(dic)
            list_pr.append(n)
            res = JsonResponse({'mess':"iteam added to your cart"})
            res.set_cookie('detail' , cook_list) 
            res.set_cookie('list_item' , list_pr)  
            return res
        

       
        
# Bug found  remember repair it
@never_cache
def cart_home(request):
    res = None
    cart_pr = None
    sum = 0
    coup = None
    pr_name = None
    reduce_amount = None
    data = None
    c = 0
    anonymous = []
   
   
    if request.COOKIES.get('detail'):
         data = literal_eval(request.COOKIES.get('detail')) 
         value = len(data)
         for i in data:
             name = i['pr_name']
             pr_na = add_product.objects.get(product_name = name)
             anonymous.append(pr_na) 
         for s in data:
            to = s['total_amount']
            print(to)
            sum = sum + int(to)
    
         print(sum)   
                        
    else:
            value = 0
           
            cart_pr = cart.objects.filter(user_name_id = request.user.id)
            coup = None
            pr_name = None
            reduce_amount = None
            anonymous = None
            c = 0
            sum = 0
            for s in cart_pr : 
                try:
                    coup = s.coupen_id.discount 
                    pr_name = s.coupen_id.product_id
                    reduce_amount = s.cupen_reduced_price
                except:
                    coup = None
                    reduce_amount = None
                    pr_name = None
                finally:    
                    print(s.prd_name) 
                    su = s.total_amount
                    print(su)
                    sum = sum + su 
                    print(sum)
                    c = cart.objects.filter( user_name_id = request.user.id).count()              
    return render(request, 'site/cart.html', {'cart_pr': cart_pr ,'total':sum , 'cart_count':c , 'coup':coup  , 'pr':pr_name , 're':reduce_amount , 'anonymous':anonymous , 'value':value, 'data':data})


def remove_from_cart(request):
    if request.user.is_authenticated:
        print("authe")
        id = request.GET.get('value')
        val = int(id)
        find = cart.objects.filter(user_name_id = request.user.id)
        for i in find:
            if i.prd_name_id == val:
                c = cart.objects.get(id = i.id)
                c.delete()
        return JsonResponse({'recieve': 'item removed from your cart'})
    else:
        lis = []
        up = []
        id = request.GET.get('value')
        val = int(id)
        pro = add_product.objects.get(id = val)
        li = literal_eval(request.COOKIES.get('list_item'))
        re= literal_eval(request.COOKIES.get('detail'))
        if len(li) == 1 :
            a = JsonResponse({'recieve': 'item removed from your cart'})
            a.delete_cookie('list_item')
            a.delete_cookie('detail')
            return a 
        else:    
            lis = [x for x in li  if x != pro.product_name]  
            up = [r for r in re  if r['pr_name'] != pro.product_name]  
            a = JsonResponse({'recieve': 'item removed from your cart'})
            a.set_cookie('list_item' , lis)
            a.set_cookie('detail' , up)
            return a 
          


def apply_coupen(request):
    
    code1 = request.GET.get('code')
    if coupens.objects.filter(coup_name  = code1).exists():
        coupen  = coupens.objects.get(coup_name  = code1)
        product_find = add_product.objects.filter(id = coupen.product_id_id)
        category_find = add_category.objects.filter(id = coupen.category_name_id)
        user_cart = cart.objects.filter(user_name_id = request.user.id)
        total = 0
        for i in product_find:
            if i.id == coupen.product_id_id :
               
                #calculation
                
                for it in user_cart:
                    if it.coupen_id_id is not None:
                        return JsonResponse({'result':'you already appliyed a coupen ('+ it.coupen_id.coup_name + ')'})
                    else:    
                        if it.coupen_id_id == coupen.id:
                            return JsonResponse({'result':"Coupen is ALready applyed"})
                        else:   
                            if coupen.product_id_id == it.prd_name_id:
                                total = it.total_amount 
                                print(total)
                                if total <= coupen.max_amount:
                                    if total >= coupen.minimum_amount:
                                        dis = (coupen.discount) /100
                                        total_discount = total * dis
                                        it.total_amount = total - int(total_discount)
                                        it.cupen_reduced_price = total_discount
                                        it.coupen_id = coupen
                                        it.save()

                                    else:
                                    
                                        return JsonResponse({"result":"coupen is applicable for mininum"+" " +  str(coupen.minimum_amount)})    
                                else:

                                    return JsonResponse({'result':"coupen is applicable for maximunm"+ str(coupen.max_amount)})                                         
                            

        for c in category_find:
            if c.id == coupen.category_name_id :
               
                #calculation
                
                for it in user_cart:
                    if it.coupen_id_id is not None:
                        return JsonResponse({'result':'you already appliyed a coupen ('+ it.coupen_id.coup_name + ')'})
                    else:    
                        if it.coupen_id_id == coupen.id:
                            return JsonResponse({'result':"Coupen is ALready applyed"})
                        else:   
                
                            if coupen.category_name_id == it.prd_name.category_name_id:
                                total = it.total_amount 
                                if total <= coupen.max_amount:
                                    if total >= coupen.minimum_amount:
                                        dis = (coupen.discount) /100
                                        total_discount = total * dis
                                        it.total_amount = total - int(total_discount)
                                        it.cupen_reduced_price = total_discount
                                        it.coupen_id = coupen
                                        it.save()

                                    else:
                                    
                                        return JsonResponse({"result":"coupen is applicable for mininum"+" " +  str(coupen.minimum_amount)})    
                                else:

                                    return JsonResponse({'result':"coupen is applicable for maximunm"+ str(coupen.max_amount)})                                         
                            
    else:
        return JsonResponse({'result':'inavalid Coupen Code...❌❌'})
    
    return JsonResponse({'result':"congratulation your coupen applyed sucessfuly🎉🎉🎉"})


def remove_coupen(request):
    cod = request.GET.get('cod')
    user_cart = cart.objects.filter(user_name_id = request.user.id)
    coup = coupens.objects.get(id = cod)
    total = 0
    for item in user_cart:
        if item.prd_name.selling_price:
           total = int(item.prd_name.selling_price) * int(item.quantity)
        else:
            total = int(item.prd_name.original_price) * int(item.quantity)    
        item.coupen_id = None
        dis = (coup.discount) /100
        total_discount = total * dis
        item.total_amount  = int(item.total_amount) + int(total_discount)
        item.save()
           

    return JsonResponse({'re':'Coupen removed sucessfully'})

def checkout(request):
    if request.user.is_authenticated:
        cart_item = cart.objects.filter(user_name_id = request.user.id)
        user_address = address.objects.filter(user_id = request.user.id)
       
        sum = 0
        for s in cart_item :  
            su = s.total_amount
            sum = sum + su 
    else:
         return redirect('/login')

    return render(request, 'site/checkout.html', {'cart_list': cart_item , 'total':sum , 'user_address':user_address})

def reazorpaycheck(request):
    cart_item = cart.objects.filter(user_name_id = request.user.id)
    sum = 0
    for s in cart_item :  
        su = s.total_amount
        sum = sum + su    
    return JsonResponse({
        'total_price':sum
    })

def add_address(request):
    if request.method == 'POST':
        user_id = User.objects.get(id = request.user.id)
        addres = address()
        addres.user_id = user_id
        first_name = request.POST.get('first-name')
        second_name = request.POST.get('last-name')
        give = first_name + ' ' + second_name
        addres.name  = give
        addres.email = request.POST.get('email')
        addres.phone_no = request.POST.get('phone')
        addres.country = request.POST.get('select')
        addres.state = request.POST.get('state')
        addres.city = request.POST.get('city')
        addres.pincode = request.POST.get('pin')
        addres.address = request.POST.get('address')
        addres.save()
        messages.success(request, 'address added sucessfully')
        return redirect('/checkout')
        
    return render(request, 'site/user_address.html')


def delete_address(request):
    num = request.GET.get('id')
    addrr = address.objects.get(id = num)
    addrr.delete()
    return JsonResponse({"msgg":"Address Deleted Sucessfully"})
    

def user_order(request):
    user_address_id = request.GET.get('address_id')
    user_payment_id = request.GET.get('payment_method')
    cart_item = cart.objects.filter( user_name_id = request.user.id)
    get_address = address.objects.get(id = user_address_id)  
    for i in cart_item:
        us_order = order()
        us_order.shipping_address = get_address
        us_order.payment_method = user_payment_id
        us_order.us_id = i.user_name
        us_order.product_id = i.prd_name 
        us_order.total_amount = i.total_amount
        us_order.quantity = i.quantity
        if i.coupen_id:
           us_order.coupen_id = i.coupen_id
        else:
            us_order.coupen_id = None 
        st = add_product.objects.get(id = i.prd_name.id)
        a = int(st.stock)
        st.stock = a - i.quantity
        st.save()
        us_order.save()

    cart_item.delete()  

    sleep(2)
    return JsonResponse({'msg':'order placed check your order History'})   

def order_page(request):
    order_item = order.objects.filter(us_id = request.user.id).order_by('-order_time__minute')
    return render(request, 'site/orderr.html' ,{'order_item':order_item})

def order_updation(request):
    order_id = request.GET.get('order_id')
    status = request.GET.get('order_up')
    text_com = request.GET.get('content')
    print(text_com)
    item = order.objects.filter(us_id = request.user.id)
    for i in item:
        i.id = order_id
        i.order_status = status
        i.complaint = text_com
        i.save()
    if status == 'return':
        return JsonResponse({'msg':'your product will be returned with in 20 Days'})   
        
    return JsonResponse({'msg':"Your Order Cancelled"})    

#remember error fix it
def search_item(request):
    query = request.GET.get('data')
    data1 = add_product.objects.filter(slug__icontains=query).values_list('slug',flat=True)
    data = add_category.objects.filter(category_name__icontains=query).values_list('category_name',flat=True)
    productlist = []
    for da1 in data1:
        productlist.append(da1)
    for da in data:
        productlist.append(da)    
    return JsonResponse({'result':productlist})

      
def search_bar(request):
    data = request.GET.get('data')
    print(data)
    get_item_pr = None
    use_page = None
    t = None
    price = request.GET.get('m_price' , '')  
    print(price)   
    if price:
        max_price = int(price.split(",",1)[0])
        min_price = int(price.split(",",1)[1])
        item = add_product.objects.filter(original_price__lte = max_price , original_price__gte = min_price)
        print(item)
        use_page = item
        t = 1
    if add_category.objects.filter(category_name = data).exists():
        c = add_category.objects.get(category_name = data)
        cat_id = c.id
        get_item_pr = add_product.objects.filter(category_name_id = cat_id) 
        page  = Paginator(get_item_pr , 2)
        page_no = request.GET.get('page')
        use_page = page.get_page(page_no)
       
    else:
        try:    
           #get_item_pr = add_product.objects.filter(product_name = data)  
            use_page = add_product.objects.filter(slug__icontains=data)
            price = request.GET.get('m_price' , '')  
            print(price)   
            if price:
                max_price = int(price.split(",",1)[0])
                min_price = int(price.split(",",1)[1])
                item = add_product.objects.filter(original_price__lte = max_price , original_price__gte = min_price)
                print(item)
                use_page = item
                t = 1
        except:
            pass
    return render(request, 'site/shop.html',{'show':use_page , 't':t})





#<.................generate otp function..................>


def generat_otp():
    global generated_otp
    generated_otp = random.randint(1000, 9999)
    send_otp(generated_otp)
    print(generated_otp)


 # <..................send opt function.........>

@csrf_exempt
def send_otp(cod):
  
   ott = cod
   service_id = "339bfc85485d407d9db9d3299105ca5b"
   token = "06036e2101a245c5b42091586a0ea4c7"
   from_ = "447520651596"
   to = "918590203684"

   headers = {
    "Authorization":f"Bearer {token}",
    "content-type":"application/json"
   }

   payload = {
    "from":from_,
    "to":[to],
    "body":ott
   }

   requests.post(
        f'https://sms.api.sinch.com/xms/v1/{service_id}/batches',
        headers=headers,
        data = json.dumps(payload)
   )