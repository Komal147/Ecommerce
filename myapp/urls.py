from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render,HttpResponse
from . import views

urlpatterns = [
    path('index',views.IndexPage,name="indexpage"),
    path('blog',views.BlogPage,name="blogpage"),
    path('category',views.CategoryPage,name="categorypage"),
    path('login',views.LoginPage,name="loginpage"),
    path('cart',views.CartPage,name="cartpage"),
    path('contact',views.ContactPage,name="contactpage"),
    path('register',views.RegisterPage,name="registerpage"),
    path('otp',views.OtpPage,name="otppage")
]
