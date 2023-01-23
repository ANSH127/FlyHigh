
from django.http import  HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages

def search(request):
    return render(request,'index.html')

def home(request):
    if request.method=='POST':
        d_country= request.POST.get('dcountry','')
        a_country=request.POST.get('acountry','')
        d_date= request.POST.get('ddate','')
        r_date=request.POST.get('rdate','null')
        adults=request.POST.get('tadults','')
        myclass=request.POST.get('myclass','')
        # print(d_country,a_country,d_date,r_date,adults,myclass)

        if d_country==a_country:
            messages.error(request,'Choose the diffrent location')
            return redirect('/')

        if d_date>r_date:
            messages.error(request,'PLease enter the correct return date')
            return redirect('/')


        
        return HttpResponse('true')
    else:
        return HttpResponse('mo')