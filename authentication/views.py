from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json 
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages


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
class RegisitrationView(View):
    def get(self,request):
        # Render the registration page template
        return render(request, 'authentication/register.html')
       
    def post(self,request):
        # messages.success(request, "Successfully Registered")
        #Get User Data
        #Validate the data
        #create user account
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
            user=User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Account Successfully Created")
            return render(request, 'authentication/register.html')
          
        return render(request, 'authentication/register.html')
 