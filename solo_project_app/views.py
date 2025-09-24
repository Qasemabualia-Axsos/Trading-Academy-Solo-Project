import requests
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Q

stripe.api_key = settings.STRIPE_SECRET_KEY


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
                # messages.success(request,'Successfully logged in !',extra_tags='login')
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

def dashboard(request):
    if 'userid' not in request.session:
        messages.error (request,'You Must LogIn First',extra_tags='login')
        return redirect ('/login_page')
    logged_user=Users.objects.get(id=request.session['userid'])
    
    data={
        'user':logged_user,
        'Courses':Courses.objects.all(),
        'Feedbacks':Feedback.objects.all(),
    }
    return render (request,'dashboard.html',data)

def logout(request):
    request.session.flush()
    return redirect ('/')

def add_feedback(request,course_id):
    if 'userid' not in request.session:
        messages.error (request,'You Must LogIn First',extra_tags='login')
        return redirect ('/login_page')
    if request.method=='POST':
        errors=Feedback.objects.feedback_validator(request.POST)
        if len (errors)>0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=f"feedback-{course_id}")
            return redirect ('/dashboard')
        logged_user=Users.objects.get(id=request.session['userid'])
        course = Courses.objects.get(id=course_id)
        Feedback.objects.create(
            user=logged_user,
            course=course,
            comment=request.POST.get('comment')
        )
        messages.success(request, "Feedback added successfully!", extra_tags=f"feedback-{course_id}")
        return redirect ('/dashboard')
    return redirect ('/dashboard')

def get_rates(request):
    url = "https://api.currencyfreaks.com/latest"
    params = {"apikey": "da0d696d119842d8aee0746a8b728773", "symbols": "EUR,GBP,JPY"}
    resp = requests.get(url, params=params).json()

    eurusd = 1 / float(resp["rates"]["EUR"])
    usdjpy = float(resp["rates"]["JPY"])
    gbpusd = 1 / float(resp["rates"]["GBP"])
    eurgbp = float(resp["rates"]["GBP"]) / float(resp["rates"]["EUR"])

    data = {
        "eurusd": round(eurusd, 5),
        "usdjpy": round(usdjpy, 3),
        "gbpusd": round(gbpusd, 5),
        "eurgbp": round(eurgbp, 5),
    }
    return JsonResponse(data)

def payment_page(request, course_id):
    if "userid" not in request.session:
        return redirect("/login_page")

    user = Users.objects.get(id=request.session["userid"])
    course = get_object_or_404(Courses, id=course_id)

 
    intent = stripe.PaymentIntent.create(
        amount=int(course.price * 100),  
        currency="usd",
        metadata={"user_id": user.id, "course_id": course.id},
    )

    return render(request, "payment_page.html", {
        "course": course,
        "user": user,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret
    })

def payment_success(request, course_id):
    if "userid" not in request.session:
        return redirect("/login_page")

    user = Users.objects.get(id=request.session["userid"])
    course = get_object_or_404(Courses, id=course_id)

    payment, created = Payment.objects.get_or_create(
        user=user,
        course=course,
        defaults={
            "status": 'completed',
            "amount": course.price
                  }
    )

    if not created:
        payment.status = 'completed'
        payment.save()

    messages.success(request, f"Payment successful! You now have access to {course.title}.")
    return redirect('/dashboard')

def lessons_page(request):
    if 'userid' not in request.session:
        messages.error (request,'You Must LogIn First',extra_tags='login')
        return redirect ('/login_page')
    logged_user=Users.objects.get(id=request.session['userid'])
    purchased_courses = Courses.objects.filter(
        payments__user=logged_user,
        payments__status="completed"
    ).distinct()
    data={
        'user':logged_user,
        'purchased_courses':purchased_courses
    }

    return render (request,'lessons.html',data)


