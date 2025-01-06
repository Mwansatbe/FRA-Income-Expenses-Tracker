from .import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
  path('validate-username', csrf_exempt(views.UserNameValidation.as_view()), name ='validate-username'),
  path('register', views.RegistrationView.as_view(), name='register'),
  path("login", views.LoginView.as_view(), name="login"),
  path('validate-email', csrf_exempt(views.EmailValidation.as_view()), name='validate-email'),
  path("activate/<uidb64>/<token>", views.VerificationView.as_view(), name= 'activate'),
  path("logout",views.LogOutView.as_view(), name="logout"),
  
]
