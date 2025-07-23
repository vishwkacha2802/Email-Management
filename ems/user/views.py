from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMessage
from django.conf import settings

def register(request):
    return render(request, 'user/register.html')


def login(request):
    return render(request, 'user/login.html')


def home(request):
    return render(request, 'user/home.html')

def store(request):
    myfname = request.POST.get("fname", "")
    mylname = request.POST.get("lname", "")
    myemail = request.POST.get("email", "")
    myusername = request.POST.get("username", "")
    mypassword = request.POST.get("password", "")
    myconfirm_password = request.POST.get("confirm_password", "")

    if mypassword == myconfirm_password:
        User.objects.create_user(
            first_name=myfname,
            last_name=mylname,
            email=myemail,
            username=myusername,
            password=mypassword
        )
        messages.success(request, "Registered Successfuly")
        return redirect('/user/login') 
    else:
        messages.error(request, "Missmatch Password")
        return redirect('/user/register')
    
def login_check(request):

    myusername = request.POST["username"]
    mypassword = request.POST["password"]

    result = auth.authenticate(username=myusername,password=mypassword)

    if result is None:

        messages.error(request, "inavlid username or password")
        return redirect('/user/login')
    else:

        auth.login(request,result)
        return redirect('/user/home')
    
def logout(request):
    auth.logout(request)
    return redirect('/user/login')    

# def email_sender(request):
#     myto = request.POST["to"]
#     mysubject = request.POST["subject"]
#     mymessage = request.POST["message"]

#     send_mail(mysubject,mymessage,settings.Email_HOST_USER,[myto])
#     messages.success(request,"Email sent: successfully..")
#     return redirect('/user/home')

def email_sender(request):

    myto = request.POST["to"]
    mysubject = request.POST["subject"]
    mymessage = request.POST["message"]
    upload_file = request.FILES.get("attachment")
    email = EmailMessage(subject=mysubject,body=mymessage,from_email=settings.EMAIL_HOST_USER,to=[myto])

    email.attach(upload_file.name, upload_file.read(), upload_file.content_type)
    email.send()
    messages.success(request, "Email Sent Successfully")
    return redirect('/user/home')