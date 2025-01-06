from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import json 
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . import utils
from django.contrib import auth 


# Email validation view class
class EmailValidation(View):
    def post(self,request):
        # Parse JSON data from the request body
        data = json.loads(request.body)
        # Extract email from the parsed data
        email = data['email']
        
        # Check if email format is valid using validate_email function
        if not validate_email(email):
            # Return 400 Bad Request if email format is invalid
            return JsonResponse({'email_error': 'email is invalid'}, status = 400)
        
        # Check if email already exists in database
        if User.objects.filter(email=email).exists():
            # Return 409 Conflict if email is already registered
            return JsonResponse({'email_error': 'Sorry email already in use choose another email'}, status = 409)
        
        # Return success response if email is valid and unique
        return JsonResponse({'email_valid': True})  


# Username validation view class
class UserNameValidation(View):
    def post(self,request):
        # Parse JSON data from the request body
        data = json.loads(request.body)
        # Extract username from the parsed data
        username = data['username']
        
        # Check if username contains only alphanumeric characters
        if not (username).isalnum():
            # Return 400 Bad Request if username contains special characters
            return JsonResponse({'username_error': 'username must only contain alphanumeric characters'}, status = 400)
        
        # Check if username already exists in database
        if User.objects.filter(username=username).exists():
            # Return 409 Conflict if username is taken
            return JsonResponse({'username_error': 'Sorry username already exists choose another name'}, status = 409)
        
        # Return success response if username is valid and unique
        return JsonResponse({'username_valid': True})  


# Registration view class for handling the registration page
class RegistrationView(View):
    def get(self,request):
        # Render the registration page template
        return render(request, 'authentication/register.html')
       
    def post(self,request):
        # messages.success(request, "Successfully Registered")
        #Get User Data
        #Validate the data
        #create user account
        
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
        "ValueFields": request.POST 
        }
        if not User.objects.filter(username=username).exists():
         if not User.objects.filter(email=email).exists():
            if len(password)<8:
              messages.error(request, "Password is too short")
              return render(request, 'authentication/register.html', context)
            user=User.objects.create_user(first_name = firstname, last_name= lastname, username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
          
            
            """
            In order to setup the link to activate the user for the website modifily the body
            1. define the path to view to verify user
            1.1 Get the domain we are on
            1.2 concatenate the relative url of the verification view to the domain
            1.3 identify user using uid, econde, decode back uid (uid user identification back and forth securely in mail process)
            1.4 get user token useed for verification only used once
            """
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            our_domain = get_current_site(request).domain
            link = reverse ("activate", kwargs={"uidb64": uidb64, "token": utils.token_generator.make_token(user)})
            activate_url =f"http://{our_domain}{link}"
            
            
            email_subject ="Acitvat Your Account"
            email_body = f"Hi {user.first_name} \nPlease use the link to verify your account {activate_url}"
            send_email ="mwansachile@gmail.com"
            recipient =email
            
            email = send_mail(
                    email_subject,
                    email_body,
                    send_email,
                    [recipient],
                    fail_silently=False,
                )
            messages.success(request, "Account Successfully Created")
            return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token ):
        
        try:
            #decode user id after activation it
            id =force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not utils.token_generator.check_token(user, token):
                messages.warning(request, "Invalid activation link or user already activated")
                return redirect("login")
            if user.is_active:
                messages.info(request, "Accounnt is already Activated")
                return redirect("login") 
            user.is_active=True
            user.save()
            messages.success(request, "Account Activated Successfully")
            return redirect("login")
        except Exception (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid Activation Link")     
        return redirect("login") 
    
    
class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")
    
    def post(self, request):
        username = request.POST["username"]
        password  = request.POST["password"]
        
        if username and password:
            user =auth.authenticate(username=username, password = password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request,f"Welcome {user.first_name}. You're logged in")
                    return redirect("expenses")
            messages.error(request, "Accoount is not active, please check email")   
            return render(request, "authentication/login.html")    
        else:
            messages.error(request, "Please fill all fields")   
            return render(request, "authentication/login.html")           
                    
                    
                    
class LogOutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect("login")
        