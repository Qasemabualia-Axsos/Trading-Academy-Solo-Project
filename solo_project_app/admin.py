from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    list_display=('title','price','created_at')
    search_fields=('title',)
    list_filter=('created_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=('title','course','order')
    list_filter=('course',)
    ordering=('course','order')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('user','course','amount','status','created_at')
    list_filter=('status','created_at')
    search_fields=('user_name','course_title')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=('user','course','comment','created_at')
    search_fields=('user_first_name','user_last_name','course_title','comment')
    list_filter=('created_at','course')