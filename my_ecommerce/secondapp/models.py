from email.policy import default
from django.db import models
from django.forms import CharField
from firstapp.models import *
# Create your models here.


class add_category(models.Model):
    category_name = models.CharField(max_length = 50, unique = True)
    slug = models.CharField(max_length = 150, null = False, blank  =False)
    image = models.ImageField(upload_to='images/')
    describtion = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.category_name

class sub_category(models.Model):
    sub_name = models.CharField(max_length = 50)
    category = models.ForeignKey(add_category,on_delete=models.CASCADE)
   
    def __str__(self):
        return self.sub_name

class add_product(models.Model):
    category_name = models.ForeignKey(add_category,on_delete=models.CASCADE)
    sub_category_name = models.ForeignKey(sub_category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 40)
    slug = models.CharField(max_length = 150, null = False, blank  =False)
    image = models.ImageField(upload_to='images/')
    imag2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')
    image4 = models.ImageField(upload_to='images/')
    describtion = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    original_price = models.IntegerField()
    selling_price = models.IntegerField(null = True)
    percentage = models.CharField(max_length = 20 , null = True)
    features = models.TextField(max_length = 700)
    stock = models.IntegerField()
    offer_reduced_price = models.IntegerField(null = True)
    

    def __str__(self):
        return self.product_name

class coupens(models.Model):
    coup_name = models.CharField(max_length = 100, unique=True)
    discount = models.IntegerField()  
    create_at = models.DateTimeField(auto_now_add=True)
    product_id =  models.ForeignKey(add_product ,on_delete = models.CASCADE , null=True) 
    category_name = models.ForeignKey(add_category,on_delete=models.CASCADE, null=True)
    max_amount = models.IntegerField()  
    minimum_amount = models.IntegerField()  
    created_at = models.DateField(auto_now_add=True)
    is_experied = models.BooleanField(default = False)
    
    def __str__(self):
        return self.coup_name

class offer(models.Model):
    product_id =  models.ForeignKey(add_product ,on_delete = models.CASCADE , null=True) 
    category_name = models.ForeignKey(add_category,on_delete=models.CASCADE, null=True)
    offer_percentage = models.IntegerField(null = True)
    total_reduction = models.IntegerField(null = True)

class cart(models.Model):
    prd_name = models.ForeignKey(add_product,on_delete = models.CASCADE)
    user_name = models.ForeignKey(User,on_delete = models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True)
    total_amount = models.BigIntegerField(null=True)
    quantity = models.IntegerField(null =True , blank = True, default= 1)
    coupen_id =  models.ForeignKey(coupens ,on_delete = models.CASCADE , null = True)
    ofer_reduced_price = models.IntegerField(null = True)
    cupen_reduced_price = models.IntegerField(null = True)

class address(models.Model):
    user_id  = models.ForeignKey(User , on_delete = models.CASCADE) 
    name = models.CharField(max_length = 100 )
    phone_no = models.CharField(max_length = 12 )
    email = models.CharField(max_length = 60  )
    country = models.CharField(max_length = 50  )
    pincode = models.CharField(max_length = 10)
    state = models.CharField(max_length = 100  )
    city = models.CharField(max_length = 80  )
    address = models.TextField(max_length = 400 )

class order(models.Model):
    us_id = models.ForeignKey(User ,on_delete = models.CASCADE)  
    product_id =  models.ForeignKey(add_product ,on_delete = models.CASCADE) 
    quantity = models.CharField(max_length = 100)
    payment_method = models.CharField(max_length = 100)
    shipping_address = models.ForeignKey(address, on_delete = models.CASCADE)
    order_status = models.CharField(max_length = 100 , default = 'pending')
    order_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.BigIntegerField()  
    coupen_id =  models.ForeignKey(coupens ,on_delete = models.CASCADE , null = True)
    complaint = models.TextField(max_length = 1000 , null = True)
    