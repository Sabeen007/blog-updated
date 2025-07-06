from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home-page'),
    path('about',views.about,name='about-page'),
    path('blog',views.blog,name='blog-page'),
    path('contact',views.contact,name='contact-page'),
    path('login',views.user_login,name='login-page'),
    path('register',views.register,name='register-page'),
    path('logout',views.user_logout,name='logout-page'),
    path('dashboard',views.dashboard,name='dashboard-page'),

]
