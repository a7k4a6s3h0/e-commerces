from . import views
from django.urls import path

urlpatterns = [

    path('',views.index1,name = 'index1'),
    path('home',views.home,name = 'home'),
    path('login',views.user_login,name = 'login'),
    path('login_otp_template',views.login_otp_template,name="login_otp_template"),
    path('render_login_page', views.render_login_page ,name='render_login_page'),
    path('login_otp',views.login_otp,name='login_otp'),
    path('signup',views.user_signup,name = 'signup'),
    path('userprofile',views.user_profile,name = 'userprofile'),
    path('edit',views.user_profile_edit,name="edit"),
    path('validate',views.validate,name ='validate'),
    path('save',views.user_details,name="save"),
    path('search-item',views.search_item,name="search-item"),
    path('search_bar',views.search_bar,name="search_bar"),
    path('logout',views.user_logout,name='logout'),
    path('shop/<str:ca>',views.shoping,name = 'shop'),
    path('pr_detail/<str:nu>/<int:n>',views.pr_detail,name = 'pr_detail'),
    #path('cart/<int:c>',views.cart1,name='cart'),
    path('get/ajax/cart',views.cart1,name='cart'),
    path('get/ajax/quantity',views.getqantity,name='quantity'),
    path('get/ajax/cart_remove',views.remove_from_cart,name='cart_remove'),
    path('cart_home',views.cart_home,name = 'cart_home'),
    #path('whislist',views.whislist,name = 'whislist'),
    path('checkout',views.checkout,name='checkout'),
    path('get/ajax/order',views.user_order,name='order'),
    path('order_page',views.order_page,name = 'order_page'),
    path('get/ajax/order_updation',views.order_updation,name='order_updation'),
    path('process-to-pay',views.reazorpaycheck,name='process-to-pay'),
    path('add_address',views.add_address,name = 'add_address'),
    path('edit_address',views.edit_address,name = 'edit_address'),
    #path('save_edit_address/<int:i>',views.save_edit_address,name='save_edit_address'),
    path('delete_address',views.delete_address,name='delete_address'),
    path('apply-coupen',views.apply_coupen,name='apply-coupen'),
    path('remove_coupen',views.remove_coupen,name="remove_coupen"),
]
