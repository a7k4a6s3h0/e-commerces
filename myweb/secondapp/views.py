
import datetime
from logging import exception
from unicodedata import category, name
from django.db.models.functions import ExtractYear 
from django.db.models.functions import ExtractDay
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache
from firstapp.models import *
from secondapp.models import add_category,add_product, order,sub_category,coupens,offer
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models import Count 
from django.db.models import Q
from django.core.paginator import Paginator
#pdf package
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#template packages

from django.http import HttpResponse
from django.views.generic import View

#excel package
import xlwt
# Create your views here.
 
def index(request):
    if request.user.is_superuser and request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
             
                return redirect('admin_home')   
        else:
            messages.error(request, 'invalid username or password')
            return redirect('/admin')   

    return render(request, 'admin-site/login.html')

@login_required(login_url='/admin')
def admin_home(request):
    if request.user.is_superuser:
        te = order.objects.annotate(
                    month=TruncMonth('order_time')
                ).values('month').annotate(
                    total_income=Sum('total_amount'),
                    
                ).order_by('month')

        tes = order.objects.annotate(
                    year=ExtractYear('order_time')
                ).values('year').annotate(
                    total_income=Sum('total_amount'),  
                ).order_by('year')        
                

        tess = order.objects.annotate(
                    day=ExtractDay('order_time')
                ).values('day').annotate(
                    total_count=Count('id'),  
                ).order_by('day')        
                

        return render(request,'admin-site/index.html',{'te':te , 'tes':tes , 'tess':tess}) 
    else:
        return redirect('/admin')



def admin_logout(request):
    logout(request)
    return redirect('/admin')

def block_user(request,num):
       if request.method == 'POST':
            user = User.objects.get(id=num)
            user.is_active = False
            user.save()
            return redirect('user_details')


def unblock_user(request,val):
    if request.method == 'POST':
       user = User.objects.get(id=val)
       print(user)
       user.is_active = True
       user.save()
       return redirect('user_details')

def user_details(request):
    if request.user.is_authenticated:
       details = User.objects.filter().order_by('id')
       return render(request, 'admin-site/user_information.html',{'details': details})     
    else:
        return redirect('/admin')

#note delete the function        
def delete_user(request,d):
    user = User.objects.get(id=d)
    user.delete()
    return redirect('user_details')

def accounts_admin(request):

    return render(request, 'admin-site/accounts.html')


def add_category1(request):
    if request.method == 'POST':
        cate = add_category()
        cate.category_name = request.POST.get('name')
        cate.describtion= request.POST.get('des')
        cate.slug = request.POST.get('slug')
        
        if len(request.FILES) !=0 :
            cate.image = request.FILES.get('image')
            print(cate.image)
            cate.save()
            return redirect('category')
        return redirect('add_category')
         
    return render(request,'admin-site/add_category.html')

def delete_category(request):
    val = request.GET.get('id')
    delete_item = add_category.objects.filter(id=val)
    delete_item.delete()
    return JsonResponse({"msg":"Category Deleted Sucessfully"})

def edit_category(request,va):
    insert_data = add_category.objects.get(id=va)   
    return render(request,'admin-site/edit_category.html',{'data':insert_data})
   
def save_edited_category(request,va):
        save_category = add_category.objects.get(id=va) 
        if request.method == 'POST':
            save_category.category_name = request.POST.get('category_name')
            save_category.describtion = request.POST.get('des')
            save_category.slug = request.POST.get('slug')
            save_category.save()
        return redirect('products')

@never_cache
def home_category(request):
    test = add_category.objects.filter()
    list_sun = sub_category.objects.filter()
    return render(request,'admin-site/category.html',{'test':test, 'list':list_sun })

def edit_sub(request,u ,ci):
    result = sub_category.objects.get(id = u)
    e  = add_category.objects.get(id= ci)
    get = add_category.objects.filter()
    return render(request,'admin-site/edit_sub.html',{'re':result , 'ed':get, 'e':e})

def save_edit_sub(request,i):
    if request.method == 'POST':
        su = sub_category.objects.get(id=i)
        va = request.POST.get('categor')
        su.category_id = add_category.objects.get(id=va)
        su.sub_name = request.POST.get('sub_category')
        su.save()
        messages.success(request, 'data saved successfuly')
        return redirect('category')
        
    else:
        messages.error(request, 'error to save data')

def delete_sub(request):
    l = request.GET.get('id')
    val = sub_category.objects.get(id =l)
    val.delete()
    return JsonResponse({"msg":'sucessfully Deleted'})


def sub_category1(request):
    list1 = add_category.objects.filter()
    if request.method == 'POST':
        take = sub_category()
        catego = request.POST.get('category')
        take.category = add_category.objects.get(id=catego)
        take.sub_name = request.POST.get('sub_category')
        take.save()
        
    return render(request,'admin-site/sub_category.html',{'list':list1})

def products(request):
    if request.user.is_authenticated:
       product_details = add_product.objects.filter()
       return render(request, 'admin-site/products.html',{ 'pro':product_details})    
    else:
        return redirect('/admin')

def edit_products(request,ed):
    edit_p = add_product.objects.get(id=ed) 
    edit_c = add_category.objects.filter()
    return render(request, 'admin-site/edit_produt.html',{'edit':edit_p, 'edit_c':edit_c})    

def loadSubCats(request):
    cat_name = request.GET.get('cat_name')
    edit_sub = sub_category.objects.filter(category_id=cat_name)
    return render(request,'admin-site/dropdown_sub.html',{'edit_sub':edit_sub})

def save_edited_products(request,op):
    data = add_product.objects.get(id=op)
    if request.method == 'POST':
        data.product_name = request.POST.get('product_name')
        data.slug = request.POST.get('slug')
        data.describtion = request.POST.get('des')
        data.original_price = request.POST.get('original_price')
        data.features = request.POST.get('features')
        data.stock = request.POST.get('stock')
        cat = request.POST.get('category_na')
        data.category_name = add_category.objects.get(id = cat)
        sub_id = request.POST.get('sub_categor')
        data.sub_category_name = sub_category.objects.get(id=sub_id)
        
            
        if data.image and data.imag2 and data.image3 and data.image4 is  None:
            messages.error(request, 'image not found')
            return redirect('products')

        elif len(request.FILES) !=0 :
            print("in")
            data.image = request.FILES.get('imag')
            data.imag2 = request.FILES.get('imag2')
            data.image3 = request.FILES.get('imag3')
            data.image4 = request.FILES.get('imag4')
            data.save()
            messages.success(request, 'product Updated sucessfully')
            return redirect('products')
        else:
            data.save()
            messages.error(request,'product Updated sucessfully')
            return redirect('products')

@never_cache           
def add_products(request):
    category_data = add_category.objects.filter()
    sub = sub_category.objects.filter()
    if request.method == 'POST':
        pro = add_product()
        category_nam = request.POST.get('category_na')
        if category_nam and category_nam != 'Select category':
           pro.category_name = add_category.objects.get(id=category_nam)
        else:
            messages.error(request,'Choose category')   
            return redirect('add_products')
        sub =request.POST.get('sub_categor')
        if sub and sub != 'Sub Category':
           pro.sub_category_name = sub_category.objects.get(id=sub)
        else:
            messages.error(request,'Choose Related Subcategory')   
            return redirect('add_products')
        pro.product_name = request.POST.get('product_name')
        pro.slug = request.POST.get('slug')
        pro.describtion = request.POST.get('des')
        pro.original_price = request.POST.get('original_price')
        pro.features = request.POST.get('features')
        pro.stock = request.POST.get('Stock')
        if len(request.FILES) !=0 :
            pro.image = request.FILES.get('imag')
            pro.imag2 = request.FILES.get('imag2')
            pro.image3 = request.FILES.get('imag3')
            pro.image4 = request.FILES.get('imag4')
            pro.save()
            messages.success(request,'data saved successfully')
            return redirect('products')
        else:
            messages.error(request, 'error to save data')
            return redirect('add_products')
    
    return render(request, 'admin-site/add-product.html',{'cat':category_data,'sub':sub})   

def delete_product(request):
    i = request.GET.get('id')
    delete_p = add_product.objects.get(id=i)
    delete_p.delete()
    return JsonResponse({"msg":"Product deleted sucessfully"})

def order_details(request):
    order_list = order.objects.filter().order_by('id')
    return render(request, 'admin-site/order_management.html',{'order_list':order_list})

def admin_updation(request):
    or_id = request.GET.get('or_id')
    status = request.GET.get('status')  
    order_item = order.objects.get(id = or_id)
    order_item.order_status = status
    order_item.save()
    return JsonResponse({'recieve':'Status updated successfully'})  

def add_coupens(request):
    return render(request, 'admin-site/add_coupen.html')

def coupen_ajax(request):
    val = request.GET.get('data')
   
    if val == "products":
        item = add_product.objects.filter().values_list('product_name',flat=True)
        
    else:
        item = add_category.objects.filter().values_list('category_name',flat=True)  

    collecter = list(item)     
    

    return JsonResponse({'result':collecter})    
    
def make_coupen(request):
    num = request.GET.get('pr') 
    name = request.GET.get('name')
    discount = request.GET.get('discount')
    max = request.GET.get('max')
    min = request.GET.get('min')
    products_get = None
    category_get = None
    
    if num:
        try:
            products_get = add_product.objects.get(product_name = num)
            if products_get is not None:
                add_coupen = coupens()
                add_coupen.coup_name = name
                add_coupen.product_id =  add_product.objects.get(id = products_get.id)
                add_coupen.discount = discount
                add_coupen.max_amount = max
                add_coupen.minimum_amount = min
                add_coupen.save()
                return JsonResponse({
                    'msg':"Coupen added successfully✅✅✅"
                })
        except:
            pass

        try:
            category_get = add_category.objects.get(category_name = num)
            if category_get is not  None:
                add_coupens = coupens()
                add_coupens.coup_name = name
                add_coupens.category_name = add_category.objects.get(id = category_get.id)
                add_coupens.discount = discount
                add_coupens.max_amount = max
                add_coupens.minimum_amount = min
                add_coupens.save()
                print("saved")
                return JsonResponse({
                    'msg':"Coupen added successfully✅✅✅"
                })
        except:
	        pass
                 
    else:
        return JsonResponse({'msg':"choose item"})
    return JsonResponse({'msg':"Coupen is already Exists"})

#remember repair
@never_cache
def coupen_home(request):
    no_coup = coupens.objects.filter().order_by("create_at__hour")
    pr_name = None
    cate_name =None
    for co in no_coup:
        
        try:
          
          pr_name = add_product.objects.get(id = co.product_id_id)
          
        except:
            pass
        try:
            cate_name = add_category.objects.get(id = co.category_name_id)
        except:
            pass        
        
    return render(request, 'admin-site/coupenmanagement.html', {'cop':no_coup , 'pr_name':pr_name , 'cat_name':cate_name})


def delete_coupen(request):
    co_name = request.GET.get('name')
    deleted_coup = coupens.objects.get(coup_name = co_name)
    deleted_coup.delete()
    return JsonResponse({'msg':'Copen deleted sucessfully'})

@never_cache        
def offer2(request):
    offer_item = offer.objects.filter()
    return render(request, 'admin-site/offer_management.html',{"offer_item":offer_item})


def add_offer(request):
    return render(request, 'admin-site/add_offer.html')

def offer_sum(request):
    item = request.GET.get('name')
    try:
       finded_item = add_product.objects.get(product_name = item)
       amount = finded_item.original_price
       pr_id = finded_item.id
    except:
        amount = None
    try:
        finded_category_item = add_category.objects.get(category_name = item)   
        pr_id = finded_category_item.id
    except:
        pass    
        
    return JsonResponse({'amount':amount , 'pr_id':pr_id})

def save_offer(request):
    given_id = request.GET.get('prid')
    offer1 = request.GET.get('offer_amount')
    reduce_amount = request.GET.get('amount_reduce') 
    selected = request.GET.get('seleted')
    if offer.objects.filter(Q(product_id_id = given_id) | Q(category_name_id = given_id)).exists():
            return JsonResponse({'res':'You already Applyeld Offer'})
       
    else: 
        if selected == 'products':  
            try: 
                pr = add_product.objects.get(id = given_id)
                offer_table = offer()
                offer_table.product_id = pr
                offer_table.offer_percentage = offer1
                offer_table.total_reduction = reduce_amount
                offer_table.save()
                based_product = add_product.objects.filter(id = pr.id)    
                off = int(offer1)
                for i in based_product:
                    old_price = int(i.original_price)
                    offer_price = off / 100
                    total = old_price * offer_price
                    final_price = old_price - total
                    i.offer_reduced_price = int(total)
                    i.percentage = offer1
                    i.selling_price = int(final_price)
                    i.save()
            except:
                pass
        else:    
            
            try:
            
                cate = add_category.objects.get(id = given_id)
                offer_table = offer()
                offer_table.category_name = cate
                offer_table.offer_percentage = offer1
                offer_table.total_reduction = reduce_amount
                offer_table.save()
                based_product = add_product.objects.filter(category_name_id = cate.id)    
                off = int(offer1)
                for i in based_product:
                    old_price = int(i.original_price)
                    offer_price = off / 100
                    total = old_price * offer_price
                    final_price = old_price - total
                    i.offer_reduced_price = int(total)
                    i.percentage = offer1
                    i.selling_price = int(final_price)
                    i.save()
                
            except:
                pass
                

    return JsonResponse({'res':"Offer Appyled Sucessfully"})

def delete_offer(request):
    offer_id = request.GET.get('offer_id')
    delete_id = offer.objects.get(id = offer_id)
    try:
      applyed_item = add_product.objects.filter(id = delete_id.product_id_id)
      for p in applyed_item:
          p.selling_price = None
          p.percentage = None
          p.offer_reduced_price = None
          p.save()
      delete_id.delete() 
    except :
        pass
    try:
        cate = add_category.objects.get(id = delete_id.category_name_id)   
        print(cate)  
        applyed_item = add_product.objects.filter(category_name_id = cate.id)
        for c in applyed_item:
            c.selling_price = None
            c.percentage = None
            c.offer_reduced_price = None
            c.save()
        delete_id.delete()
    except:
        pass
    return JsonResponse({'msg':"Offer Deleted Sucessfully"})           

def sale(request):
    order_table = order.objects.filter().order_by('-order_time')
    try:
        page_no = request.GET.get('page')
        if int(page_no) == 2:
            #order_table = order.objects.annotate(month=TruncMonth("order_time")).values("month").order_by("month")
            order_table = order_table = order.objects.filter().order_by('order_time__month')
    except:
        page_no = 0
    return render(request , 'admin-site/sales_report.html',  {'sales_report':order_table , 'no':int(page_no)})


def pd(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    choose = request.GET.get('exampleRadios')
    if from_date and to_date is not None:
        if choose == 'pdf':
            date_input = from_date
            datetimeobject = datetime.datetime.strptime(date_input,'%m/%d/%Y')
            new_format = datetimeobject.strftime('%Y-%m-%d')
            date_input2 = to_date
            datetimeobject2 = datetime.datetime.strptime(date_input2,'%m/%d/%Y')
            new_format2 = datetimeobject2.strftime('%Y-%m-%d')
            order_details = order.objects.filter(order_time__range=[new_format, new_format2])
        
            sum = 0
            for s in order_details:
                if s.order_status != 'cancle' or s.order_status != 'return':
                    sum = sum + s.total_amount

            if order_details:
                template_path = 'admin-site/pdf.html' 
                context = {'data':order_details, 'total':sum}
                # Create a Django response object, and specify content_type as pdf
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                # find the template and render it.
                template = get_template(template_path)
                html = template.render(context)
                # create a pdf
                pisa_status = pisa.CreatePDF(
                html, dest=response)
                # if error then show some funny view
                
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                
                return response

        else:
            
            date_input = from_date
            datetimeobject = datetime.datetime.strptime(date_input,'%m/%d/%Y')
            new_format = datetimeobject.strftime('%Y-%m-%d')
            date_input2 = to_date
            datetimeobject2 = datetime.datetime.strptime(date_input2,'%m/%d/%Y')
            new_format2 = datetimeobject2.strftime('%Y-%m-%d')
            order_details = order.objects.filter(order_time__range=[new_format, new_format2]) 
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="users.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('users Data') # this will make a sheet named Users Data

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['username', 'Product Name', 'Quantity', ' Address', 'payment_method' , 'total_amount' ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            rows = []
            for i in order_details:
                rows.append((i.us_id.username , i.product_id.product_name , i.quantity , i.shipping_address.address , i.payment_method , i.total_amount )) 
            
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response


    else:
        messages.error(request, 'Please Choose date')
        return redirect('sales_report')

   



#<....................pdf generated function.......................>



