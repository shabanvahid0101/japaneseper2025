
# courses/admin.py
from django.contrib import admin
from .models import Course, Content

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')  # ستون‌های نمایش
    list_filter = ('instructor', 'created_at')  # فیلترها
    search_fields = ('title', 'description')  # جستجو

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'content_type', 'created_at')
    list_filter = ('course', 'content_type')
    search_fields = ('title',)