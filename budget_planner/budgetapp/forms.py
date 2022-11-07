from django.forms import ModelForm
from .models import Category, Expense


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['username']


class CategoryExpense(ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount']
        exclude = ['category']
