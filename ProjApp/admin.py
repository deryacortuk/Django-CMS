from django.contrib import admin
from .models import Topic, Category, Module

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}
class ModuleInline(admin.StackedInline):
    model = Module
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'view']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

