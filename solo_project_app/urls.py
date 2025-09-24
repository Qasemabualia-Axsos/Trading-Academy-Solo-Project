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
    path('api/rates/', views.get_rates, name='get_rates'),
    path("payment/<int:course_id>/", views.payment_page, name="payment_page"),
    path("payment-success/<int:course_id>/", views.payment_success, name="payment_success"),
    path('lessons_page',views.lessons_page,name='lessons_page'),


]

    
