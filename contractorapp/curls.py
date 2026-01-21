from django.urls import path
from . import views


urlpatterns = [

path('contarctordash/',views.contractordash,name='contractordash'),
path('contractorlogout/',views.contractorlogout,name='contractorlogout'),
path('contractorchangepassword/',views.contractorchangepassword,name='contractorchangepassword'),
path('contractorprofile/',views.contractorprofile,name='contractorprofile'),
path('contractoredit/',views.contractoredit,name='contractoredit'),
path('contractorviewprojects/',views.contractorviewprojects,name='contractorviewprojects'),
path('applyproject/<id>',views.applyproject,name='applyproject'),
path('contractorapplications/',views.contractorapplications,name='contractorapplications'),
path('assignedprojects/',views.assignedprojects,name='assignedprojects'),
path('addprogress/<id>',views.addprogress,name='addprogress'),

]