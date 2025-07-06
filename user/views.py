from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import ProfileImageForm, BlogForm
from .models import Profile, ProfileImage, Blog, Category
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Blog, Category, Pages
from .forms import BlogForm
from .models import Pages
from .forms import PageForm


@login_required
def profile(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName', '').strip()
        lastName = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        contact = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        image = request.FILES.get('image')

        if not all([firstName, lastName, email, contact, address]):
            messages.error(request, "All fields are required.")
            return redirect('profile-page')
        
        # Update User model
        user = request.user
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.save()
        
        # Update or create Profile model
        profile, created = Profile.objects.get_or_create(user=user)
        profile.contact = contact
        profile.address = address
        profile.save()

        if image:
            ProfileImage.objects.create(user_id=user.id, image=image)
            
        messages.success(request, "Profile created successfully." if created else "Profile updated successfully.")
        return redirect('profile-page')   

    profile_images = list(ProfileImage.objects.filter(user=request.user).order_by('-id'))
    active_image = next((img for img in profile_images if img.status == 1), None)

    return render(request, 'user/profile.html', {
        'profile_images': profile_images,
        'latest_image': active_image, 
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            
        return redirect('profile-page')
        
    return redirect('profile-page')                   


@login_required
def activate_profile_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        selected_image = get_object_or_404(ProfileImage, id=image_id, user=request.user)

       
        ProfileImage.objects.filter(user=request.user).exclude(id=selected_image.id).update(status=0)

        selected_image.status = 1
        selected_image.save()

        return redirect('profile-page')

    return redirect('profile-page')


@login_required
def page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        image = request.FILES.get('image')
        status = request.POST.get('status')
        description = request.POST.get('description')
        
        if not title or not status or not description:
            messages.error(request,"All Fields Are Required")
            return redirect('pages-page')
        
        Pages.objects.create(title=title, slug=slug, image=image, status=status, description=description)
        messages.success(request,'Pages Created Successfully')
        return redirect('pageslist-page')

    return render(request, 'user/pages.html')

@login_required
def pageslist(request):
    pages = Pages.objects.all()
    return render(request, 'user/pageslist.html',{'pages':pages})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pages
from .forms import PageForm

@login_required
def edit_page(request, pk):
    page = get_object_or_404(Pages, pk=pk)

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('pageslist-page')
    else:
        form = PageForm(instance=page)

    return render(request, 'user/editpage.html', {'form': form, 'page': page})


@login_required
def delete_page(request, pk):
    page = get_object_or_404(Pages, pk=pk)
    if request.method == 'POST':
        page.delete()
        messages.success(request, "Page deleted successfully.")
        return redirect('pageslist-page')  # Update this to your actual page list URL name
    # For safety, you can show a confirmation page or redirect
    return redirect('pageslist-page')


@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'user/bloglist.html', {'blogs': blogs})


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect('bloglist-page')

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm(instance=blog)

    return render(request, 'user/editblog.html', {'form': form, 'blog': blog})


@login_required
def blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category_id')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        category = Category.objects.get(id=category_id)

        if not title or not category_id or not description:
            messages.error(request,'All fields are Required')
            return redirect('blog-create-page') 

        Blog.objects.create(title=title, slug=slug, category=category,image=image,description=description)
        messages.success(request,'Blog Created Successfully')
        return redirect('bloglist-page')
       
    categories = Category.objects.all()
    return render(request, 'user/blog.html', {'categories': categories})

@login_required
def categories(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id')

        if name:
            if category_id:
                category = Category.objects.get(id=category_id)
                category.name = name
                category.save()
                messages.success(request, "Category updated successfully.")
            else:    
                Category.objects.create(name=name)
                messages.success(request, 'Category created successfully!')
        else:
            messages.error(request, 'Name field is required.')
        return redirect('categories-page')
    
    categories = Category.objects.all().order_by('-id')
    return render(request, 'user/categories.html', {'categories': categories})

@require_POST
@login_required
def delete_blog(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        blog.delete()
        return redirect('bloglist-page')

@require_POST
@login_required
def delete_category(request):
    category_id = request.POST.get('category_id')
    try:
        Category.objects.get(id=category_id).delete()
        messages.success(request, "Category deleted.")
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
    return redirect('categories-page')


@login_required
def contact(request):
    return render(request, 'user/contact.html')


