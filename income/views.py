from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from . models import Source, Income
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date
import datetime

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/authentication/login")
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)





@login_required(login_url="/authentication/login")
def index(request):
    sources = Source.objects.all()  # Get all sources
    income = Income.objects.filter(owner=request.user)  # Filter incomes by the logged-in user
    
    # Get user preferences with default currency handling
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = 'ZMW - Zambian Kwacha'  # Default currency if preferences don't exist
    
    # Create a paginator object with 10 items per page
    paginator = Paginator(income, 10)
    
    # Get the page number from the GET parameters
    page_number = request.GET.get('page')
    
    # Get the page object for the current page number
    page_obj = paginator.get_page(page_number)
    
    context = {
        "income": income,
        "page_obj": page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)
  
  
  
  
  
@login_required(login_url="/authentication/login")
def add_income(request):
  sources = Source.objects.all()
  context ={
     "sources": sources,
     "values": request.POST
   }
  
  if request.method=="GET":
    return render(request, 'income/add-income.html', context)
    
   
  if request.method=="POST":
   amount=request.POST['amount']
  #  import pdb
  #  pdb.set_trace()
   if not amount:
    messages.error(request,'Amount is required')
    return render(request, 'income/add-income.html', context)
  
  source=request.POST['source']
  description=request.POST['description']
  date=request.POST['income_date']
 
  
  
  if not description:
     messages.error(request,'Description is required')
     return render(request, 'income/add-income.html', context)
   
  Income.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
  messages.success(request, 'Record Saved Successfully')
  
  return redirect('income')






@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit-income.html', context)
        
        # Parse the date from string to date object
        income_date_parsed = parse_date(date)
        if not income_date_parsed:
            messages.error(request, 'Invalid date format')
            return render(request, 'income/edit-income.html', context)

        # Update the expense
        income.owner = request.user
        income.amount = amount
        income.date = income_date_parsed
        income.source = source
        income.description = description
        
        income.save()
        messages.success(request, 'Record updated successfully')

        return redirect('income')







# @login_required(login_url="/authentication/login")
# def income_edit(request, id):
#     # Fetch the income and categories
#     income = get_object_or_404(Income, pk=id)
#     sources = Source.objects.all()

#     if request.method == "GET":
#         context = {
#             'income': income,
#             'values': income,
#             'sources': sources,
#         }
#         print(f"GET Request Context: {context}")  # Debugging
#         return render(request, "income/edit-income.html", context)

#     elif request.method == "POST":
#         # Form data and validation
#         amount = request.POST.get('amount')
#         description = request.POST.get('description')
#         source = request.POST.get('source')
#         income_date = request.POST.get('income_date')

#         if not all([amount, description, source, income_date]):
#             messages.error(request, "All fields are required!")
#             context = {
#                 'income': income,
#                 'values': {
#                     'amount': amount,
#                     'description': description,
#                     'category': source,
#                     'income_date': income_date,
#                 },
#                 'sources': sources,
#             }
#             print(f"POST Request Context: {context}")  # Debugging
#             return render(request, "income/edit-income.html", context)

#         # Save changes
#         income.owner = request.user
#         income.amount = amount
#         income.description = description
#         income.source = source
#         income.income_date = income_date
#         income.save()

#         messages.success(request, "Record updated successfully")
#         return redirect('income')  # Redirect to the income list view










      
# @login_required(login_url="/authentication/login")
# def income_edit(request, id):
#     # Fetch the income and categories
#     income = get_object_or_404(Income, pk=id)
#     sources = Source.objects.all()

#     if request.method == "GET":
#         # Pre-fill the form with existing values
#         context = {
#             'income': income,
#             'values': income,
#             'sources': sources,
#         }
#         return render(request, "income/edit-income.html", context)

#     elif request.method == "POST":
#         # Get form data
#         amount = request.POST.get('amount')
#         description = request.POST.get('description')
#         source = request.POST.get('source')
#         income_date = request.POST.get('income_date')

#         # Validation checks
#         if not amount or not description or not source or not income_date:
#             messages.error(request, "All fields are required!")
#             context = {
#                 'income': income,
#                 'values': {
#                     'amount': amount,
#                     'description': description,
#                     'category': source,
#                     'expense_date': income_date,
#                 },
#                 'sources': sources,
#             }
#             return render(request, "income/edit-income.html", context)

#         # Update the income object
#         income.owner=request.user
#         income.amount = amount
#         income.description = description
#         income.source = source
#         income.income_date = income_date
#         income.save()

#         # Success message and redirect
#         messages.success(request, "Record updated successfully")
#         return redirect('income')  # Replace 'income' with the correct URL name


@login_required(login_url="/authentication/login")  
def delete_income(request, id):
    # Safely retrieve the income object or return a 404 error if it doesn't exist
    income = get_object_or_404(Income, pk=id)
    
    # Delete the income
    income.delete()
    
    # Display a success message to the user
    messages.success(request, 'Income Record removed successfully.')
    
    # Redirect to the income list page
    return redirect('income')
  
  
def income_sources_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    income = Income.objects.filter(
        owner=request.user,
        date__gte=six_months_ago, 
        date__lte=todays_date
    )
    
    finalrep = {}
    
    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source, income)))
    
    # Calculate total for each source
    for source in source_list:
        filtered_by_source = income.filter(source=source)
        amount = sum(item.amount for item in filtered_by_source)
        finalrep[source] = amount
    
    return JsonResponse({"income_source_data": finalrep}, safe=False)
        

def stats_view(request):
    return render(request, 'income/stats.html')