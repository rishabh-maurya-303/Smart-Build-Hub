from django.shortcuts import render,redirect
from django.contrib import messages
from sbhapp.models import *
from . forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import *
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'tp': Project.objects.all().count(),
        'top': Project.objects.filter(status="under_construction").count(),
        'tcp': Project.objects.filter(status="completed").count(),
        'tpa': Project.objects.filter(status="awaiting_approval").count(),
        'tpp': Project.objects.filter(status="planned").count(),
        'dp': Project.objects.filter(status="designing_phase").count(),
        'tdp': Project.objects.filter(status="delayed").count(),
        'tpc': Project.objects.filter(status="cancelled").count(),
    }
    return render(request,'homeownerdash.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('signin')
    else:
        return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerchangepassword(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try : 
            homeowner =LoginInfo.objects.get(username=homeownerid)
            if homeowner.password != oldpwd:
                messages.error(request,"Old password is incorrect")
                return redirect('homeownerchangepassword')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Confirm Password Are not Same")
                return redirect('homeownerchangepassword')
            elif homeowner.password == newpwd:
                messages.error(request,"New Password is same as Old Password")
                return redirect('homeownerchangepassword')
            else:
                homeowner.password = newpwd
                homeowner.save()
                messages.success(request,"Password changed successfully")
                return redirect('homeownerdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Something Went Wrong")
            return redirect('signin')
    return render(request,'homeownerchangepassword.html',{'homeownerid':homeownerid})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    return render(request,'homeownerprofile.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        homeowner.name = name
        homeowner.contactno = contactno
        homeowner.address = address
        homeowner.bio = bio
        if profile:
            homeowner.picture=profile
        homeowner.save()
        messages.success(request,"Your Profile has been updated")
        return redirect('homeownerprofile')
    return render(request,'homeowneredit.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'form':form,
    }
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request,"Project has been added")
            return redirect('addproject')
        else:
            messages.error(request,"Invalid Form")
            return redirect('addproject')
    return render(request,'addproject.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerviewprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'homeownerviewprojects.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
    }
    return render(request,'homeownerviewapplications.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    app.status = 'rejected'
    app.save()
    messages.success(request,"Application have been rejected")
    return redirect('homeownerviewapplications',id=app.project.id)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approveapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    project = Project.objects.get(id=app.project.id)
    apps = ContractorApplication.objects.filter(project=app.project).update(status="rejected")
    app.status = 'approved'
    app.save()
    project.contractor = app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request,"Application have been Approved")
    return redirect('homeownerviewapplications',id=app.project.id)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def runningprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='under_construction')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'runningprojects.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'updates':updates,
    }
    return render(request,'viewupdates.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownercompletedprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='completed')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request,'homeownercompletedprojects.html',context)