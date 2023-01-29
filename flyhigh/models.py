from django.db import models
from django.utils.timezone import now

# Create your models here.



class Flight(models.Model):
    sno=models.AutoField(primary_key=True)
    plane_name=models.CharField(max_length=20)
    plane_code = models.CharField(max_length=10)
    # week=models.CharField(max_length=200)
    origin=models.CharField(max_length=20)
    origin_airport = models.CharField(max_length=64)
    origin_code=models.CharField(max_length=10)
    destination=models.CharField(max_length=20)
    destination_code=models.CharField(max_length=10)
    destination_airport = models.CharField(max_length=64)
    depart_time=models.TimeField(blank=True)
    arrival_time=models.TimeField(blank=True)
    flight_duration=models.CharField(max_length=20,default='')
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    
class Booking(models.Model):
    sno=models.AutoField(primary_key=True)
    passengar_details=models.CharField(max_length=500,default='')
    flight_info=models.ForeignKey(Flight,on_delete=models.CASCADE)
    country_code=models.CharField(max_length=10)
    mob_no=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    amount=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    flight_d_date=models.CharField(max_length=30)
    flight_a_date=models.CharField(max_length=30)
    return_flight_d_date=models.CharField(max_length=50,default='')
    return_flight_a_date=models.CharField(max_length=50,default='')
    status=models.CharField(max_length=10,default='')


    def __str__(self):
        return "Order id "+str(self.sno)+" STATUS- "+self.status
