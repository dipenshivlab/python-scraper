from django.contrib import admin
from . models import *
from django.urls import reverse
from django.utils.html import escape, mark_safe
from django.utils.html import format_html_join,format_html
from django.urls import path
from clutch_company.views import get_review
from django.contrib.auth.models import User,Group


class CompanyAdmin(admin.ModelAdmin):

    list_display = ['company_name','website','location','position','get_related']
    list_display_links=['get_related']
    list_per_page=9
    actions = None
    
    # change_list_template=""

    # def get_related(self, instance):
    #     print("instance",instance)
    #     obj = instance.company_review.all()
        
    #     return format_html_join(
    #         ',',
    #         '<a href="{}">{}</a>',
    #         ((
    #             reverse('admin:clutch_company_review_change', args=(c.id,)), 
    #             c.client_name
    #         ) for c in obj),
    #     )
    # get_related.short_description = 'Related Reviews'

    def has_add_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Company Records'} # Here
        return super().changelist_view(request, extra_context=extra_context)

    def get_related(self, instance):
        company_id = instance.id
        review_url = reverse("review", kwargs={'company_id': company_id})
        return format_html('<a href="{}">Show Reviews</a>', review_url)

    get_related.short_description = 'Related Reviews'


class ReviewAdmin(admin.ModelAdmin):
    def company_link(self, obj):
        link=reverse("admin:clutch_company_company_change", args=[obj.company.id]) #model name has to be lowercase
        return mark_safe(f'<a href="%s">%s</a>' % (link,obj.company.company_name))
    
    company_link.allow_tags=True
    company_link.short_description = 'company_name'

    list_display = ['client_name','client_company','position','company_link',]
    list_display_links=['company_link']
    list_per_page=20
    

admin.site.register(Company,CompanyAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
# admin.site.register(Review,ReviewAdmin)
