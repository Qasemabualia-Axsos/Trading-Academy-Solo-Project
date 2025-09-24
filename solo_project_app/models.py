from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt

# Create your models here.
class usersManager(models.Manager):
    def user_validator(self,postData):
        errors={}
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

        if not postData['first_name']:
            errors['first_name_empty']='First Name is Empty'
        else:
            if len(postData['first_name'])<2:
                errors['first_name_len']='First Name must be more than 2 characters'

        if not postData['last_name']:
            errors['last_name_empty']='Last Name is Empty'
        else:
            if len(postData['last_name'])<2:
                errors['last_name_len']='Last Name must be more than 2 characters'

        if not postData['email']:
            errors['email_empty']='Email is Empty'
        elif not EMAIL_REGEX.match(postData['email']):
                errors['email']='Invalid email address'
             
        elif Users.objects.filter(email=postData['email']).exists():
            errors['email_exist']="Email already registered"
        
        if not postData['password'] or not postData['confirm_PW']:
            errors['password_empty']='Paswsord is Empty'
        else:
            if len(postData['password'])<8:
                errors['password_len']='Password should be more than 8 characters'
            else:
                if postData['password'] != postData['confirm_PW']:
                    errors['password_confirm']='Password not match'
        return errors

    def login_validator(self,postData):
        errors={}

        if not postData['email']:
            errors['email_empty']='Email is Empty'

        if not postData['password']:
            errors['password_empty']='Passord is Empty'

        if not postData['user_email']:
            errors['password_confirm']='Invalid Email or Password'

        return errors

class Users(models.Model):
   
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=255 , unique=True)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=usersManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Courses(models.Model):
    title=models.CharField(max_length=45)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title}'

class Lesson(models.Model):
    course=models.ForeignKey(Courses,related_name='lessons',on_delete=models.CASCADE)
    title=models.CharField(max_length=45)
    video_url=models.URLField()
    order=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.order}'
    

class Payment(models.Model):
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed')
    )
    user=models.ForeignKey(Users,related_name='payments',on_delete=models.CASCADE)
    course=models.ForeignKey(Courses,related_name='payments',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=45,choices=STATUS_CHOICES,default='pending')
    strip_session_id=models.CharField(max_length=255,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.course.title}'
    
    class Meta:
        unique_together=('user','course')

    def __str__(self):
        return f'{self.user.first_name}  enrolled in {self.course.title}  ' 

class feedbackManager(models.Manager):
    def feedback_validator(self,postData):
        errors={}
        if not postData['comment']:
            errors['comment_empty']="commnt is Empty"
        elif len (postData['comment'])< 5:
            errors['comment_len']='Comment Must Be More Than 5 Characters'
        return errors


class Feedback(models.Model):
    user=models.ForeignKey(Users,related_name='feedbacks',on_delete=models.CASCADE)
    course=models.ForeignKey(Courses,related_name='feedbacks',on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=feedbackManager()

    def __str__(self):
        return f'{self.comment}'
    
