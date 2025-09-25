import requests
from django.shortcuts import render,redirect,HttpResponse
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
from django.contrib.auth.decorators import login_required

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
        messages.error(request,'You Must LogIn First',extra_tags='login')
        return redirect('/login_page')

    logged_user = Users.objects.get(id=request.session['userid'])

    # Fetch initial rates safely
    url = "https://v6.exchangerate-api.com/v6/34e15b3da3713185fe1988ce/latest/USD"
    data = requests.get(url).json()

    usd_to_eur = eur_to_usd = None  # default values
    conversion_rates = data.get('conversion_rates')
    if conversion_rates:
        usd_to_eur = round(conversion_rates.get('EUR', 0), 5)
        eur_to_usd = round(1 / usd_to_eur, 5) if usd_to_eur else 0
    else:
        # Optional: log or display error message
        messages.warning(request, f"Forex API error: {data.get('error-type', 'Unknown error')}")

    context = {
        'user': logged_user,
        'Courses': Courses.objects.all(),
        'Feedbacks': Feedback.objects.all(),
        'initial_rates': {
            'usd_to_eur': usd_to_eur,
            'eur_to_usd': eur_to_usd
        }
    }
    return render(request, 'dashboard.html', context)

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

import datetime

def currency_data(request):
    labels = []
    prices = []

    today = datetime.date.today()
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        url = f"https://api.exchangerate.host/{date}"
        params = {"base": "USD", "symbols": "EUR"}
        response = requests.get(url, params=params).json()
        
        if "rates" in response:
            labels.append(str(date))
            prices.append(response["rates"]["EUR"])

    labels.reverse()
    prices.reverse()

    return JsonResponse({"labels": labels, "prices": prices})

import requests
from django.shortcuts import render

import requests
from django.shortcuts import render


def get_forex_rates(request):
    url = "https://v6.exchangerate-api.com/v6/34e15b3da3713185fe1988ce/latest/USD"
    response = requests.get(url)
    data = response.json()

    # Check if the API returned an error
    if data.get('result') == 'error':
        return JsonResponse({'error': data.get('error-type', 'Unknown error')})

    # Safe access
    conversion_rates = data.get('conversion_rates')
    if not conversion_rates:
        return JsonResponse({'error': 'Conversion rates not available'})

    usd_to_eur = conversion_rates.get('EUR')
    eur_to_usd = 1 / usd_to_eur

    return JsonResponse({
        'usd_to_eur': usd_to_eur,
        'eur_to_usd': eur_to_usd
    })


def api_courses(request):
    courses=list(Courses.objects.values('id','title','description','price'))
    return JsonResponse({'courses':courses})

def search_lessons(request):
    query = request.GET.get('q', '').strip()
    user_id = request.session.get('userid')

    if not user_id:
        return JsonResponse({'lessons': []})  # not logged in

    # Only get courses the user has purchased
    purchased_courses = Courses.objects.filter(
        payments__user_id=user_id,
        payments__status="completed"  # make sure this matches your Payment.status
    ).distinct()

    # Only get lessons from those courses
    lessons = Lesson.objects.filter(
        course__in=purchased_courses,
        title__icontains=query
    )

    data = {
        'lessons': [
            {
                'id': lesson.id,
                'title': lesson.title,
                'description': getattr(lesson, 'description', ''),
                'course_id': lesson.course.id
            }
            for lesson in lessons
        ]
    }
    return JsonResponse(data)



def view_course(request,course_id):
    if 'userid' not in request.session:
        messages.error(request,'You Must LogIn First',extra_tags='login')
        return redirect('/login_page')

    logged_user = Users.objects.get(id=request.session['userid'])
    course=Courses.objects.get(id=course_id)
    context = {
        'user': logged_user,
        'course': course,
        'Feedbacks': Feedback.objects.all(),
    }
    return render(request, 'courses.html', context)
