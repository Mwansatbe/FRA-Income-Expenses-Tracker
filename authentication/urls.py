from .import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
  path('validate-username', csrf_exempt(views.UserNameValidation.as_view()), name ='validate-username'),
  path('register', views.RegisitrationView.as_view(), name='register'),
  path('validate-email', csrf_exempt(views.EmailValidation.as_view()), name='validate-email'),
]
