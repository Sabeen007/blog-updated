from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import Blog,Pages

# Create your views here.
def home(request):
    blogs = Blog.objects.order_by('-id')[:5]
    return render(request,'home/index.html',{'blogs':blogs})

def about(request):
    return render(request,'home/about.html')

def blog(request):
    blogs = Blog.objects.all()
    return render(request,'home/blog.html',{'blogs':blogs})

def pagedetail(request,slug):
    page=Pages.objects.get(slug=slug)
    return render(request,'home/pagedetail.html',{'page':page})

def blog_detail(request,slug):
    blog=Blog.objects.get(slug=slug)
    return render(request, 'home/blogdetail.html', {'blog': blog})

def contact(request):
    return render(request,'home/contact.html')

def user_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "All fields are required")
            return redirect('login-page')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard-page')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login-page')
    
    return render(request,'home/login.html')

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstname')
        lastName =request.POST.get('lastname')
        email =request.POST.get('email')
        password =request.POST.get('password')
        confirmPassword =request.POST.get('confirmpassword') 
        
        if not all([firstName,lastName,email,password,confirmPassword]):
            messages.error(request, "all field are required.")
            return redirect('register-page')
        
        if password != confirmPassword:
            messages.error(request, "password do not match.")
            return redirect('register-page')
 
        if User.objects.filter(username=email).exists   ():
            messages.error(request,"Email is already registered.")
            return redirect('register-page')
        
        User.objects.create_user(
            username=email,
            password=password,
            first_name=firstName,
            last_name=lastName,
        )

        messages.success(request, "Account created successfully.")
        return redirect('login-page')

    return render(request,'home/register.html')

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('login-page') 

@login_required
def dashboard(request):
    return render(request,'user/dashboard.html')

