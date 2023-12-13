from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from clutch_company.clutch import newFile
from django.contrib import admin
from . models import Review
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

login_url="/admin/login/"
# Create your views here.
@login_required(login_url=login_url)
def helloworld(request):
    return HttpResponse("Hello World")

@login_required(login_url=login_url)
def service_info(request):
    available_apps = admin.site.get_app_list(request)
    context = {
        'available_apps': available_apps,
    }
    if request.method == 'POST':
        webURL = request.POST.get('url')
        pageCount = request.POST.get('page')
        customizeFileName = request.POST.get('position')
        newFile(webURL, pageCount, customizeFileName)
        return HttpResponseRedirect(request.path_info)
    return render(request,'company_scraper.html',context)

@login_required(login_url=login_url)
def get_review(request,company_id):
    reviews=Review.objects.filter(company=company_id)
    paginator = Paginator(reviews, 10)  # Assuming 10 items per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page=1
        page_obj=paginator.get_page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
        
    available_apps = admin.site.get_app_list(request)
    context = {'reviews':page_obj,'available_apps': available_apps,}
    return render(request,'custom_review_list.html',context=context)
    