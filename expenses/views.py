from django.shortcuts import render, redirect
from . models import Category, Expense
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/authentication/login")
def index(request):
  categories = Category.objects.all()
  expenses=Expense.objects.filter(owner=request.user)
  context={
    "expenses": expenses
  }
  return render(request, 'expenses/index.html', context)

def add_expense(request):
  categories = Category.objects.all()
  context ={
     "categories": categories,
     "values": request.POST
   }
  
  if request.method=="GET":
    return render(request, 'expenses/add-expense.html', context)
    
   
  if request.method=="POST":
   amount=request.POST['amount']
  #  import pdb
  #  pdb.set_trace()
   if not amount:
    messages.error(request,'Amount is required')
    return render(request, 'expenses/add-expense.html', context)
  
  category=request.POST['category']
  description=request.POST['description']
  date=request.POST['expense_date']
 
  
  
  if not description:
     messages.error(request,'Description is required')
     return render(request, 'expenses/add-expense.html', context)
   
  Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
  messages.success(request, 'Expenses Saved Successfully')
  
  return redirect('expenses')
  
  
  
 
 
 

  
