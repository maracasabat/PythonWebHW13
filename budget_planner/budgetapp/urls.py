from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('category/', views.category, name='category'),
    path('expenses/', views.expenses, name='expenses'),
    path('report/', views.report, name='report'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
]