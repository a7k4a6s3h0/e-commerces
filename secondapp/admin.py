from django.contrib import admin
from secondapp.models import add_category, add_product, sub_category
# Register your models here.

admin.site.register(add_category)
admin.site.register(add_product)
admin.site.register(sub_category)