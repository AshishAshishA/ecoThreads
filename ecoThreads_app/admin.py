from django.contrib import admin
from .models import Category, City, Area, Address, Orders

# Register your models here.

admin.site.register(Category)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Address)
admin.site.register(Orders)
