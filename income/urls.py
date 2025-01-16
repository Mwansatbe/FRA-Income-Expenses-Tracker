from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
  path('', views.index, name='income'),
  path('add-income',views.add_income, name='add-income'),
  path('edit-income/<int:id>', views.income_edit, name='edit-income'),
  path('delete-income/<int:id>', views.delete_income, name='delete-income'),
  path('search-income', csrf_exempt(views.search_income), name='search_income'),
  path("income_sources_summary", views.income_sources_summary, name="income_sources_summary"),
  path("stats-view", views.stats_view, name ="stats-view"),
  path('export-csv', views.export_csv, name="export-csv"),
  path('export-excel', views.export_excel, name="export-excel"),
  path('export-pdf', views.export_pdf, name="export-pdf"),
]