
from django.http import  HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from flyhigh.models import Flight
import datetime,json
from . models import Booking,Userdetails

import random
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum


from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


MERCHANT_KEY = 'EAf_iZOj19wu#B5q'


# Create your views here.

def check(request):
    return render(request,'pdfreport.html')


def flights(request):
    global params
    if request.method=='POST':
        d_country= request.POST.get('dcountry','')
        a_country=request.POST.get('acountry','')
        d_date= request.POST.get('ddate','')
        r_date=request.POST.get('rdate','null')
        adults=request.POST.get('tadults','')
        myclass=request.POST.get('myclass','')
        print(d_country,a_country,d_date,r_date,adults,myclass)
        if d_country==a_country:
            messages.error(request,'Choose the diffrent location')
            return redirect('/')

        if d_date>r_date and len(r_date)>=1:
            messages.error(request,'PLease enter the correct return date')
            return redirect('/')
        
        

        print('r',len(r_date))
        flight=Flight.objects.filter(origin_code=d_country,destination_code=a_country)
        params={'flight':flight,'myclass':myclass,'d_country':d_country,'a_country':a_country,'d_date':d_date,'r_date':r_date,'adults':adults}
        if r_date=='null' or len(r_date)==0: 
            return render(request,'home.html',params)
        
        else:
            flight2=Flight.objects.filter(origin_code=a_country,destination_code=d_country)
            params={'flight':flight,'flight2':flight2,'myclass':myclass,'d_country':d_country,'a_country':a_country,'d_date':d_date,'r_date':r_date,'adults':adults}
        
            return render(request,'home2.html',params)

    else:
        return HttpResponse('mo')


def home(request):
    return render(request,'search.html')


def filter(request):
    
    global params
    if request.method=='POST':
        range=request.POST.get('range','')
        d1= request.POST.get('dbtn','')
        a1=request.POST.get('abtn','')
        d_con=request.POST.get('d_con','')
        a_con=request.POST.get('a_con','')
        f_class=request.POST.get('f_class','')
        print(range,d1,d_con,a_con,a1,f_class)
        if f_class=='Economy':
            flight=Flight.objects.filter(origin_code=d_con,destination_code=a_con,economy_fare__lte=range)
        if f_class=='Business':
            flight=Flight.objects.filter(origin_code=d_con,destination_code=a_con,business_fare__lte=range)
        if f_class=='First Class':
            flight=Flight.objects.filter(origin_code=d_con,destination_code=a_con,first_fare__lte=range)
        
        if d1=='1':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,depart_time__lt='06:00:00')
            
        if d1=='2':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,depart_time__gte='06:00:00',depart_time__lte='12:00:00',)
            print(f1)
        
        if d1=="3":
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,depart_time__gte='12:00:00',depart_time__lte='18:00:00',)
        
        if d1=='4':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,depart_time__gte='18:00:00',)

        if d1!='1' and d1!='2' and d1!='3' and d1!='4':
            f1=flight

        flight=flight.intersection(f1)
        
        if a1=='1':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,arrival_time__lt='06:00:00')
            
        if a1=='2':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,arrival_time__gte='06:00:00',arrival_time__lte='12:00:00',)
            
        
        if a1=="3":
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,arrival_time__gte='12:00:00',arrival_time__lte='18:00:00',)
        
        if a1=='4':
            f1=Flight.objects.filter(origin_code=d_con,destination_code=a_con,arrival_time__gte='18:00:00',)

        if a1!='1' and a1!='2' and a1!='3' and a1!='4':
            f1=flight

        flight=flight.intersection(f1)

        for i in params:
            if i=='flight':
                params[i]=flight
        
        return render(request,'home.html',params)


            
    return HttpResponse('hi')



def review(request,myid):
    global params,key1,info
    if len(params['r_date'])>0 and params['r_date']!='null':
        lst=myid.split(',')
        # print(lst)
        f1=Flight.objects.filter(sno=lst[0])
        f2=Flight.objects.filter(sno=lst[1])
        print(f1)
        print(f2)
        if len(params['d_date'])>0:
            t_passenger=params['adults']
            f_class=params['myclass']
            d_date=params['d_date']
            r_date=params['r_date']
            # for first flight
            yy=int(d_date[:4])
            mm=int(d_date[5:7])
            dd=int(d_date[8:])
            x = datetime.datetime(yy, mm, dd)
            d_date1=x.strftime("%a %b %d %Y")
            dt_date1=str(f1[0].depart_time)
            at_date1=str(f1[0].arrival_time)
            y=datetime.time(int(dt_date1[:2]),int(dt_date1[3:5]),int(dt_date1[6:]))
            y1=y.strftime("%p")
            z=datetime.time(int(at_date1[:2]),int(at_date1[3:5]),int(at_date1[6:]))
            z1=z.strftime("%p")
            if y1=='PM' and z1=='AM':
                x1=datetime.datetime(yy,mm,dd+1)
                a_date1=x1.strftime("%a %b %d %Y")

            else:
                a_date1=d_date1

        
            if f_class=='Economy':
                amount1=f1[0].economy_fare
            elif f_class=="Business":
                amount1=f1[0].business_fare
        
            else:
                amount1=f1[0].first_fare

            print(amount1)
            print(d_date1,a_date1)

        
        

            # for second flight

            print(r_date)
            yy1=int(r_date[:4])
            mm1=int(r_date[5:7])
            dd1=int(r_date[8:])
            x1 = datetime.datetime(yy1, mm1, dd1)
            d_date2=x1.strftime("%a %b %d %Y")
            dt_date2=str(f2[0].depart_time)
            at_date2=str(f2[0].arrival_time)
            y_1=datetime.time(int(dt_date2[:2]),int(dt_date2[3:5]),int(dt_date2[6:]))
            y2=y_1.strftime("%p")
            z_1=datetime.time(int(at_date2[:2]),int(at_date2[3:5]),int(at_date2[6:]))
            z2=z_1.strftime("%p")
            if y2=='PM' and z2=='AM':
                x3=datetime.datetime(yy1,mm1,dd1+1)
                a_date2=x3.strftime("%a %b %d %Y")

            else:
                a_date2=d_date2

        
            if f_class=='Economy':
                amount2=f2[0].economy_fare
            elif f_class=="Business":
                amount2=f2[0].business_fare
        
            else:
                amount2=f2[0].first_fare

            print(amount2)
            print(d_date2,a_date2)

            
            params1={'flightinfo':f1[0],'flightinfo2':f2[0],'d_date':d_date1,'a_date':a_date1,'d_date2':d_date2,'a_date2':a_date2,'amt':amount1+amount2,'t_passenger':t_passenger,'myid':lst[0],'myid2':lst[1],'f_class':f_class}
            return render(request,'booking2.html',params1)
        
        

            
           

        return HttpResponse('yay')
    else:
        print(params['d_date'],len(params['r_date']),params['myclass'],params['adults'])
        f1=Flight.objects.filter(sno=myid)
        if len(params['d_date'])>0:
            t_passenger=params['adults']
            f_class=params['myclass']
            d_date=params['d_date']
            yy=int(d_date[:4])
            mm=int(d_date[5:7])
            dd=int(d_date[8:])
            x = datetime.datetime(yy, mm, dd)
            d_date1=x.strftime("%a %b %d %Y")
            dt_date1=str(f1[0].depart_time)
            at_date1=str(f1[0].arrival_time)
            y=datetime.time(int(dt_date1[:2]),int(dt_date1[3:5]),int(dt_date1[6:]))
            y1=y.strftime("%p")
            z=datetime.time(int(at_date1[:2]),int(at_date1[3:5]),int(at_date1[6:]))
            z1=z.strftime("%p")
            if y1=='PM' and z1=='AM':
                x1=datetime.datetime(yy,mm,dd+1)
                a_date1=x1.strftime("%a %b %d %Y")

            else:
                a_date1=d_date1

        
            if f_class=='Economy':
                amount=f1[0].economy_fare
            elif f_class=="Business":
                amount=f1[0].business_fare
        
            else:
                amount=f1[0].first_fare

            print(amount)
        
        
        
        # print(y1,z1)
        # print(f1[0].depart_time,f1[0].arrival_time)
        print(f1[0].destination)
        params1={'flightinfo':f1,'d_date':d_date1,'a_date':a_date1,'amt':amount,'t_passenger':t_passenger,'myid':myid,'f_class':f_class}
        return render(request,'booking.html',params1)


def handlerequest(request):
    global bookingid,myinfo
    print(request.user)
    if request.method=='POST':
        
        hash = random.getrandbits(128)

        passengar_details=request.POST.get('p_Json','')
        contact_details=request.POST.get('c_Json','')
        flight_id=request.POST.get('myid','')
        flight_class=request.POST.get('myclass','')
        flight_d_date= request.POST.get('d_date','')
        flight_a_date= request.POST.get('a_date','')
        flight_d_date2= request.POST.get('d_date2','')
        flight_a_date2= request.POST.get('a_date2','')
        Amount=request.POST.get('amount','')
        val=contact_details.split(" ")
        mob=val[0]
        email=val[1]
        c_code=val[2]

        if len(flight_id.split(','))==1: 
            print(flight_id.split(','))
            f1=Flight.objects.filter(sno=flight_id)
            f3=f1
        else:
            lst=flight_id.split(',')
            f1=Flight.objects.filter(sno=lst[0])
            f2=Flight.objects.filter(sno=lst[1])
            f3=f1.union(f2)
            print(f3)




        # print(passengar_details)
        dict=json.loads(passengar_details)
        
        # print(dict)
        booking=Booking(passengar_details=passengar_details,flight_info=f1[0],country_code=c_code,mob_no=mob,email=email,amount=Amount,flight_d_date=flight_d_date,flight_a_date=flight_a_date,return_flight_d_date=flight_d_date2,return_flight_a_date=flight_a_date2)
        booking.save()
        bookingid=booking.sno
        user_1=Userdetails(user=request.user,bookinginfo=Booking.objects.filter(sno=bookingid)[0])
        user_1.save()

        myinfo={'passenger':dict,'mob':mob,'c_code':c_code,'email':email,'flightdata':f3,'flight_d_date':flight_d_date,'amount':Amount,'flight_a_date':flight_a_date,'flight_class':flight_class,'return_flight_d_date':flight_d_date2,'return_flight_a_date':flight_a_date2}
        param_dict = {

                'MID': 'hDSsMm33439078158954',
                'ORDER_ID': str(hash+bookingid),
                'TXN_AMOUNT': str(Amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest1/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})



    return HttpResponse('hi')

@csrf_exempt
def handlerequest1(request):
    global bookingid
    print(bookingid)
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            Booking.objects.filter(sno=bookingid).update(status='True')
            return render(request,'success.html')


        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            Booking.objects.filter(sno=bookingid).update(status='False')
            return render(request,'fail.html')


    return render(request, 'paymentstatus.html', {'response': response_dict})
    # return HttpResponse('done')




def create_pdf(request):
    global myinfo
    mob=(myinfo['mob'])
    email=myinfo['email']
    d_date=myinfo['flight_d_date']
    a_date=myinfo['flight_a_date']
    d_date2=myinfo['return_flight_d_date']
    a_date2=myinfo['return_flight_a_date']
    amount=myinfo['amount']
    pdetails=myinfo['passenger']
    
    

    template_path = 'pdfreport.html'
    context = {'information':myinfo['flightdata'],'mob':mob,'email':email,'d_date':d_date,'a_date2':a_date2,'d_date2':d_date2,'a_date':a_date,'amount':amount,'now':datetime.datetime.now(),'basicfare':int(amount)-100,'pdetails':pdetails,'flight_class':myinfo['flight_class']}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="ticket.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
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

    

def handleSignup(request):
    if request.method=='POST':
        # get the post parameter
        username=request.POST.get('username','')
        name=request.POST.get('name','')
        signup_email=request.POST.get('signup_email','')
        password=request.POST.get('password','')
        password1=request.POST.get('password1','')
        print(username,name,signup_email,password,password1)
        fname=name.split()[0]
        lname=name.split()[1]
        # username should be atleast 10 character long
        if len(username)>10:
            messages.error(request,'username must be under 10 characters')
            return redirect('/')
        # username should be alphanumeric
        
        if not  username.isalnum():
            messages.error(request,'username should only cantain letters and number')
            return redirect('/')
        # password should be match with confirm password field
        if password!=password1:
            messages.error(request,'Password does not match')
            return redirect('/')

        
        myuser=User.objects.create_user(username,signup_email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your FlyHigh account successfully created")
        return redirect('/')


    else:
        return render(request,'signup.html')


def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST.get('username','')
        loginpassword=request.POST.get('password','')
        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials, Please Try Again')
            return redirect('/')



        
    else:
        return render(request,'login.html')


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logout')
    return redirect('/')
    


def mybooking(request):
    val=(request.user)
    if str(val)!="AnonymousUser":
       myuser=Userdetails.objects.filter(user=request.user)
       params={'flight':myuser}
       return render(request,"mybookings.html",params)
    
    else:
        return render(request,'login.html')