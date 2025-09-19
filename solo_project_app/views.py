from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def home(request):
    return render (request,'home.html')

def login_page(request):

    return render (request,'login.html')

def register_page(request):

    return render (request,'register.html')

def login(request):
    if request.method=='POST':
        user=Users.objects.filter(email=request.POST.get('email')).first()
        
        if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
                request.session['userid']=user.id
                request.session['first_name']=user.first_name
                messages.success(request,'Successfully logged in !',extra_tags='login')
                return redirect('/dashboard')
        else:
            messages.error(request,'Invalid email or password',extra_tags='login')
            return redirect('/login_page')

def register(request):
    if request.method=='POST':
        errors=Users.objects.user_validator(request.POST)
        if len(errors)>0:
            for feild ,error in errors.items():
                messages.error(request,error,extra_tags=feild)
            return redirect('/register_page')

        else:
            password=request.POST.get('password')
            pw_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    
        Users.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                password=pw_hash
        )
        request.session['first_name']=request.POST.get('first_name')
        messages.success(request,'Successfully create User',extra_tags='register')
        return redirect('/register_page')
    return redirect('/register_page')