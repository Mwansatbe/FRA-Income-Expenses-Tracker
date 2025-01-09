from django.shortcuts import render, redirect
from . models import Category, Expense
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from userpreferences.models import UserPreferences



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/authentication/login")
def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)



@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()  # Get all categories
    expenses = Expense.objects.filter(owner=request.user)  # Filter expenses by the logged-in user
    
    currency = UserPreferences.objects.get(user=request.user).currency

    # Create a paginator object with 5 items per page
    paginator = Paginator(expenses, 10)

    # Get the page number from the GET parameters
    page_number = request.GET.get('page')

    # Get the page object for the current page number
    page_obj = paginator.get_page(page_number)

    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)
  
# def index(request):
#   categories = Category.objects.all()
#   expenses=Expense.objects.filter(owner=request.user)
#   paginator=Paginator(expenses, 5)
#   page_number= request.GET.get('page')
#   page_obj=Paginator.get_page(paginator, page_number)
  
#   context={
#     "expenses": expenses,
#     "page_obj": page_obj
#   }
#   return render(request, 'expenses/index.html', context)

@login_required(login_url="/authentication/login")
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
          
      
@login_required(login_url="/authentication/login")
def expense_edit(request, id):
    # Fetch the expense and categories
    expense = get_object_or_404(Expense, pk=id)
    categories = Category.objects.all()

    if request.method == "GET":
        # Pre-fill the form with existing values
        context = {
            'expense': expense,
            'values': expense,
            'categories': categories,
        }
        return render(request, "expenses/edit-expense.html", context)

    elif request.method == "POST":
        # Get form data
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        expense_date = request.POST.get('expense_date')

        # Validation checks
        if not amount or not description or not category or not expense_date:
            messages.error(request, "All fields are required!")
            context = {
                'expense': expense,
                'values': {
                    'amount': amount,
                    'description': description,
                    'category': category,
                    'expense_date': expense_date,
                },
                'categories': categories,
            }
            return render(request, "expenses/edit-expense.html", context)

        # Update the expense object
        expense.owner=request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.expense_date = expense_date
        expense.save()

        # Success message and redirect
        messages.success(request, "Expense updated successfully")
        return redirect('expenses')  # Replace 'expenses' with the correct URL name


@login_required(login_url="/authentication/login")  
def delete_expense(request, id):
    # Safely retrieve the expense object or return a 404 error if it doesn't exist
    expense = get_object_or_404(Expense, pk=id)
    
    # Delete the expense
    expense.delete()
    
    # Display a success message to the user
    messages.success(request, 'Expense removed successfully.')
    
    # Redirect to the expenses list page
    return redirect('expenses')
  
  
  
 
 
 

  
