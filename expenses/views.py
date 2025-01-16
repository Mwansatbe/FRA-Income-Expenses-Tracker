from django.shortcuts import render, redirect
from . models import Category, Expense
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from userpreferences.models import UserPreferences
from django.utils.dateparse import parse_date
import datetime
import csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
from django.conf import settings
import base64
import os

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
    # Get all categories (if needed for filtering or additional context)
    categories = Category.objects.all()

    # Get all expenses for the logged-in user
    expenses = Expense.objects.filter(owner=request.user)

    # Try to get user preferences or create a new one if not present
    try:
        user_preferences = UserPreferences.objects.get(user=request.user)
    except UserPreferences.DoesNotExist:
        # If no preferences found, create a new one with default 'USD' currency
        user_preferences = UserPreferences.objects.create(user=request.user, currency='ZMW - Zambian Kwacha')

    # Get the currency from user preferences
    currency = user_preferences.currency

    # Paginate the expenses (10 items per page)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for the template
    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": currency,
        "categories": categories,
    }
    return render(request, 'expenses/index.html', context)


# @login_required(login_url="/authentication/login")
# def index(request):
#     categories = Category.objects.all()  # Get all categories
#     expenses = Expense.objects.filter(owner=request.user)  # Filter expenses by the logged-in user
    
#     currency = UserPreferences.objects.get(user=request.user).currency

#     # Create a paginator object with 5 items per page
#     paginator = Paginator(expenses, 10)

#     # Get the page number from the GET parameters
#     page_number = request.GET.get('page')

#     # Get the page object for the current page number
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "expenses": expenses,
#         "page_obj": page_obj,
#         'currency': currency
#     }
#     return render(request, 'expenses/index.html', context)
  
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



@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        # Parse the date from string to date object
        expense_date_parsed = parse_date(date)
        if not expense_date_parsed:
            messages.error(request, 'Invalid date format')
            return render(request, 'expenses/edit-expense.html', context)

        # Update the expense
        expense.owner = request.user
        expense.amount = amount
        expense.date = expense_date_parsed
        expense.category = category
        expense.description = description
        
        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expenses')
    
    
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
  
    
    
    
    
    
    
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses =Expense.objects.filter(owner=request.user,date__gte=six_months_ago, date__lte=todays_date)
    
    finalrep={
        
    }
    
    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))
    def get_expense_category_amount(category):
        amount =0
        filtered_by_category=expenses.filter(category=category)
        for item in filtered_by_category:
            amount+=item.amount
        return amount
    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)
    return JsonResponse({"expense_category_data": finalrep}, safe=False)
        

def stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response ["Content-Disposition"]="Attachment; filename=Expense"+str(datetime.datetime.now())+ ".csv"
    writer=csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses =Expense.objects.filter(owner=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response
    
    
    

def export_excel(request):
    response=HttpResponse(content_type="application/ms-excel")
    response ["Content-Disposition"]="Attachment; filename=Expense"+str(datetime.datetime.now())+ ".xls"
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Expenses")
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    
    columns =['Amount', 'Description', 'Category', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style=xlwt.XFStyle()
    rows =Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    
    for row in rows:
        row_num+=1
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num,str(row[col_num]), font_style)
            
    wb.save(response)
    return response
        
    
    

def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; attachment; filename=Expenses_" + str(datetime.datetime.now()) + ".pdf"
    
    # Get the user's expenses and calculate total
    expenses = Expense.objects.filter(owner=request.user)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Convert image to base64
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo-main-1.png')
    with open(logo_path, 'rb') as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Generate HTML
    html_string = render_to_string('expenses/pdf-output.html', {
        'expenses': expenses,
        'total': total,
        'logo_base64': logo_base64
    })
    
    # Generate PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    result = html.write_pdf()
    
    response.write(result)
    return response
    
    
    
    
    
    
    
    
    
          
      
# @login_required(login_url="/authentication/login")
# def expense_edit(request, id):
#     # Fetch the expense and categories
#     expense = get_object_or_404(Expense, pk=id)
#     categories = Category.objects.all()

#     if request.method == "GET":
#         # Pre-fill the form with existing values
#         context = {
#             'expense': expense,
#             'values': expense,
#             'categories': categories,
#         }
#         return render(request, "expenses/edit-expense.html", context)

#     elif request.method == "POST":
#         # Get form data
#         amount = request.POST.get('amount')
#         description = request.POST.get('description')
#         category = request.POST.get('category')
#         expense_date = request.POST.get('expense_date')

#         # Validation checks
#         if not amount or not description or not category or not expense_date:
#             messages.error(request, "All fields are required!")
#             context = {
#                 'expense': expense,
#                 'values': {
#                     'amount': amount,
#                     'description': description,
#                     'category': category,
#                     'expense_date': expense_date,
#                 },
#                 'categories': categories,
#             }
#             return render(request, "expenses/edit-expense.html", context)

#         # Update the expense object
#         expense.owner=request.user
#         expense.amount = amount
#         expense.description = description
#         expense.category = category
#         expense.expense_date = expense_date
#         expense.save()

#         # Success message and redirect
#         messages.success(request, "Expense updated successfully")
#         return redirect('expenses')  # Replace 'expenses' with the correct URL name



  
  
 
 
 

  
