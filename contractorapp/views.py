from django.shortcuts import render,redirect
from django.contrib import messages
from sbhapp.models import *
from homeownerapp.models import *
from .models import *
from decimal import Decimal
from django.views.decorators.cache import cache_control
from homeownerapp.models import Project, UserInfo


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractordash(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()

    my_applications = ContractorApplication.objects.filter(contractor=contractor)
    assigned_projects_count = my_applications.filter(status='approved').exclude(project__status='completed').count()
    completed_projects_count = my_applications.filter(status='approved', project__status='completed').count()

    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'total_applications': my_applications.count(),
        'approved_applications': my_applications.filter(status='approved').count(),
        'pending_applications': my_applications.filter(status='pending').count(),
        'rejected_applications': my_applications.filter(status='rejected').count(),
        
        # Project metrics 
        'assigned_projects': assigned_projects_count,
        'completed_projects': completed_projects_count,
        
        # Marketplace metrics (assuming 'planned' means open for bidding)
        'new_projects_available': Project.objects.filter(status='planned').count(),
        
        # Rating placeholders
        'avg_rating': 0, 
        'feedback_count': 0,
    }
    return render(request,'contractordash.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorlogout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('signin')
    else:
        return redirect('signin')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorchangepassword(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try : 
            contractor =LoginInfo.objects.get(username=contractorid)
            if contractor.password != oldpwd:
                messages.error(request,"Old password is incorrect")
                return redirect('contractorchangepassword')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Confirm Password Are not Same")
                return redirect('contractorchangepassword')
            elif contractor.password == newpwd:
                messages.error(request,"New Password is same as Old Password")
                return redirect('contractorchangepassword')
            else:
                contractor.password = newpwd
                contractor.save()
                messages.success(request,"Password changed successfully")
                return redirect('contractordash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Something Went Wrong")
            return redirect('signin')
    return render(request,'contractorchangepassword.html',{'contractorid':contractorid})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorprofile(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
    }
    return render(request,'contractorprofile.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractoredit(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        contractor.name = name
        contractor.contactno = contactno
        contractor.address = address
        contractor.bio = bio
        if profile:
            contractor.picture=profile
        contractor.save()
        messages.success(request,"Your Profile has been updated")
        return redirect('contractorprofile')
    return render(request,'contractoredit.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorviewprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=None)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects,
    }
    return render(request,'contractorviewprojects.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def applyproject(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project,
    }
    application = ContractorApplication.objects.filter(project=project,contractor=contractor)
    if application.exists():
        messages.warning(request,"You have already applied for this application")
        return redirect('contractorviewprojects')
    if request.method == "POST":
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget = request.POST.get('estimated_budget')
        try:
            estimated_budget = Decimal(estimated_budget)
        except:
            messages.error(request,"Invalid estimated budget")
            return redirect('contractorviewprojects')
        estimated_duration = request.POST.get('estimated_duration')
        app = ContractorApplication(
            contractor=contractor,
            project=project,
            proposal_text=proposal_text,
            design_file=design_file,
            estimated_budget=estimated_budget,
            estimated_duration=estimated_duration,
        )
        app.save()
        messages.success(request,'Project Application Submited Successfully')
        return redirect('contractorviewprojects')
    return render(request,'applyproject.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorapplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    applications = ContractorApplication.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'applications':applications,
    }
    return render(request,'contractorapplications.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def assignedprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects,
    }
    return render(request,'assignedprojects.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addprogress(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project,
    }
    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        image = request.FILES.get('image')
        progress_percent = int(request.POST.get('progress_percent'))
        pu = ProgressUpdate(project=project,update_text=update_text,image=image,progress_percent=progress_percent,updated_by=contractor)
        if progress_percent > 100:
            messages.error(request,"Progress cannot be greater than 100%")
            return redirect('addprogress',id=id)
        elif progress_percent < 0 or progress_percent <progress_percent:
            messages.error(request,"Progress cannot be less than 0%")
            return redirect('addprogress',id=id)
        if progress_percent == 100:
            project.status = 'completed'
        project.progress = progress_percent
        project.save()
        pu.save()
        messages.success(request,"Progress Updated Successfully")
        return redirect('assignedprojects')
    return render(request,'addprogress.html',context)