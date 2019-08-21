from django.db import models


class Categories(models.Model):
    category_name = models.CharField(max_length=200, unique=False)

    def __str__(self):
        return self.category_name


class Connect(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    expense_item_name = models.CharField(max_length=100, unique=True)


