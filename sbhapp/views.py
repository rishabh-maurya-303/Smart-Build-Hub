from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import requests
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request,'index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        enq = Enquiry(name = name,contactno = contactno,email = email, subject = subject, message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request,"Your Enquiry Have Been Submited Successfully.")
        return redirect('contact')
    return render(request,'contact.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def about(request):
    return render(request,'about.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def services(request):
    return render(request,'services.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def projects(request):
    return render(request,'projects.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try :
            log = LoginInfo.objects.get(username=username,password=password)
            if log is not None:
                if log.usertype.lower() == "homeowner":
                    request.session['homeownerid'] = username
                    messages.success(request,"Welcome Homeowner")
                    return redirect('homeownerdash')
                elif log.usertype.lower() == "contractor":
                    request.session['contractorid'] = username
                    messages.success(request,"Welcome Contractor")
                    return redirect('contractordash')
                else :
                    messages.error(request,"Something Went Wrong")
                    return redirect('signin')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid Username or password")
            return redirect('signin')
    return render(request,'signin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        usertype = request.POST.get('usertype')
        password = request.POST.get('password')
        u = LoginInfo.objects.filter(username=email)
        if u:
            messages.error(request,"Email already exists")
            return redirect('signup')
        log = LoginInfo(usertype=usertype,username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"Account Created  Successfully")
    return render(request,'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def aboutdev(request):
    return render(request,'aboutdev.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            ad = LoginInfo.objects.get(username = username,password = password, usertype="admin")
            if ad is not None :
                request.session['adminid'] = username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')

