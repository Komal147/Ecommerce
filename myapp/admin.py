from django.contrib import admin
from . models import Customertbl,Producttbl,Carttbl,Transactiontbl

# Register your models here.
admin.site.register(Customertbl)
admin.site.register(Producttbl)
admin.site.register(Carttbl)
admin.site.register(Transactiontbl)