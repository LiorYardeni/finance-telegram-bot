from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= "index"),
    path('categories', views.categories, name="categories"),
    # path('categories_table', views.categories_table, name = 'categories_table'),
    path('connect', views.connect_expense_to_category, name="connect")
]
