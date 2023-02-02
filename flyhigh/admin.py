from django.contrib import admin
from flyhigh.models import Flight,Booking,Userdetails
# Register your models here.
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Userdetails)