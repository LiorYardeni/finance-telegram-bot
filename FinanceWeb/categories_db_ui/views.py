from django.shortcuts import render
from categories_db_ui.forms import InsertToDb, ConnectExpenseToCategory


def index(request):
    my_dict = {"insert_me": "index.html"}
    return render(request, "categories_db_ui/index.html", context=my_dict)


def categories(request):
    form = InsertToDb()

    if request.method == 'POST':
        form = InsertToDb(request.POST)

        if form.is_valid():
            print("form validation confirmed")
            form.save()

    return render(request, 'categories_db_ui/categories_form.html', context={"form": form})


def connect_expense_to_category(request):
    connect_form = ConnectExpenseToCategory()

    if request.method == "POST":
        connect_form = ConnectExpenseToCategory(request.POST)

        if connect_form.is_valid():
            connect_form.save()

    return render(request, "categories_db_ui/connect_expense_to_category.html", context={"form": connect_form})
