from django import forms

from categories_db_ui.models import Categories, Connect


class InsertToDb(forms.ModelForm):

    class Meta:
        model = Categories
        fields = "__all__"


class ConnectExpenseToCategory(forms.ModelForm):

    class Meta:
        model = Connect
        fields = "__all__"
