from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['id','Title','Description','Location','Status','Created','Posted_by']
