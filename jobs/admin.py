from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner')
    list_filter = ('location', 'owner__role')


admin.site.register(JobListing)

admin.site.register(JobApplication)
