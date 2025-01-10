from django.contrib import admin
from . models import Income, Source
# Register your models here.





class IncomeAdmin(admin.ModelAdmin):
    list_display = ("amount", "description", "owner", "source", "date")
    search_fields = ("description", "source", "date")
    
    # Add filters to the sidebar for numeric and date fields
    list_filter = ("source", "date", "amount")
    
    list_per_page=5

admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)






# class IncomeAdmin(admin.ModelAdmin):
#   list_display=("amount", "description", "owner", "source", "date")
#   search_fields=("description", "source", "date")
# admin.site.register(Income, IncomeAdmin)
# admin.site.register(Source)
