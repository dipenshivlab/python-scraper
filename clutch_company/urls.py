from django.contrib import admin
from django.urls import path
from clutch_company.views import helloworld,service_info,get_review

urlpatterns = [
    path('hello/', helloworld,name='hello_world'),
    path('service/',service_info,name='service'),
    path('get-review/<company_id>',get_review,name='review')
]
