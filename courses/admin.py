from django.contrib import admin

from .models import Course, Subject, Module

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.TabularInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ['title', 'subjects', 'created']
    list_filter = ['subjects', 'created']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

