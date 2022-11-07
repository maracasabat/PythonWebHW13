from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Expense, User
from .forms import CategoryForm, CategoryExpense
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime


# Create your views here.
def main(request):
    category = Category.objects.all()
    return render(request, 'budgetapp/index.html', {'category': category})


@login_required
def category(request):
    if request.method == 'POST':
        try:
            form = CategoryForm(request.POST)
            category = form.save(commit=False)
            category.user_id = request.user
            category.save()
            return redirect(to='/')
        except ValueError as err:
            return render(request, 'budgetapp/category.html',
                          {'form': CategoryForm, 'error': err})
    return render(request, 'budgetapp/category.html', {'form': CategoryForm()})


@login_required
def expenses(request):
    category = Category.objects.filter(user_id=request.user).all()
    if request.method == 'POST':
        try:
            name = request.POST['name']
            amount = request.POST['value']
            category = request.POST['category']
            expense = Expense(name=name, amount=amount, user_id=request.user)
            expense.save()
            expense.category.add(category)
        except ValueError as err:
            return render(request, 'budgetapp/expenses.html', {'categories': category, 'error': err})
        except IntegrityError:
            return render(request, 'budgetapp/expenses.html', {'categories': category, 'error': 'Name must be unique'})

    return render(request, 'budgetapp/expenses.html', {'categories': category})


@login_required
def report(request):
    if request.method == 'POST':
        first_date = request.POST.get('first_date')
        end_date = request.POST.get('end_date')
        try:
            first_date = datetime.strptime(first_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            first_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
            end_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
        rep = Expense.objects.filter(user_id=request.user).filter(date_now__range=[first_date, end_date]).aggregate(Sum('amount'))
        exp = Expense.objects.filter(user_id=request.user).filter(date_now__range=[first_date, end_date])
        income = 0
        outcome = 0
        for _ in exp:
            if _.amount >= 0:
                income = income + _.amount
            else:
                outcome = outcome + _.amount
        return render(request, 'budgetapp/report.html',
                      {'first_date': first_date, 'end_date': end_date, 'rep': rep['amount__sum'], 'income': income,
                       'outcome': outcome})
    else:
        return render(request, 'budgetapp/report.html', {})


def signup(request):
    if request.method == 'GET':
        return render(request, 'budgetapp/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('signin')
            except IntegrityError:
                return render(request, 'budgetapp/signup.html',
                              {'form': UserCreationForm(), 'error': 'Username already exist!'})

        else:
            return render(request, 'budgetapp/signup.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'budgetapp/signin.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'budgetapp/signin.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password did not match'})
        login(request, user)
        return redirect('main')


@login_required
def signout(request):
    logout(request)
    return redirect('main')
