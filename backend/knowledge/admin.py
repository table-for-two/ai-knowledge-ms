from django.contrib import admin

from knowledge.models import KnowledgeBase


# Register your models here.
@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
