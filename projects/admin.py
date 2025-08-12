from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    last_display=('id','name','created_by','created_at')
    search_fields=('name','description')
    list_filter=('created_at',)