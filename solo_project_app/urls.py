from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('login_page',views.login_page,name='login_page'),
    path('register_page',views.register_page,name='register_page'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('add_feedback/<int:course_id>',views.add_feedback,name='add_feedback'),
    path("currency-data/", views.currency_data, name="currency_data"),
    path("payment/<int:course_id>/", views.payment_page, name="payment_page"),
    path("payment-success/<int:course_id>/", views.payment_success, name="payment_success"),
    path('lessons_page',views.lessons_page,name='lessons_page'),
    path('api/get_forex_rates/', views.get_forex_rates, name='get_forex_rates'),
    path('api/courses/', views.api_courses, name='api_courses'),
    path('search_lessons/', views.search_lessons, name='search_lessons'),
    path('view_course/<int:course_id>',views.view_course,name='view_course')






]

    
