from django.contrib import admin
from . models import Expense, Category
# Register your models here.



class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "description", "owner", "category", "date")
    search_fields = ("description", "category", "date")
    
    # Add filters to the sidebar for numeric and date fields
    list_filter = ("category", "date", "amount")
    list_per_page=5

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)




# class ExpenseAdmin(admin.ModelAdmin):
#   list_display=("amount", "description", "owner", "category", "date")
#   search_fields=("amount", "description", "owner", "category", "date")

# admin.site.register(Expense, ExpenseAdmin)
# admin.site.register(Category)
