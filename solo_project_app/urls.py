from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('login_page',views.login_page,name='login_page'),
    path('register_page',views.register_page,name='register_page')
    
]
