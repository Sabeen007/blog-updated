from django.urls import path
from . import views

urlpatterns = [
    path('pages/', views.page, name='pages-page'),
    path('profile/', views.profile, name='profile-page'),
    path('categories/', views.categories, name='categories-page'),
    path('contact/', views.contact, name='admin-contact-page'),
    path('pageslist/', views.pageslist, name='pageslist-page'),
    path('admin/pages/edit/<int:pk>/', views.edit_page, name='edit-page'),
    path('admin/pages/delete/<int:pk>/', views.delete_page, name='delete-page'),
    path('admin/blogs/', views.blog_list, name='bloglist-page'),
    path('admin/blog/create/', views.blog, name='blog-create-page'),
    path('admin/blog/edit/<int:blog_id>/', views.edit_blog, name='admin-edit-blog'),
    path('change_password/', views.change_password, name='change-password'),
    path('delete_category/', views.delete_category, name='delete-category'),
    path('activate-profile-image/', views.activate_profile_image, name='activate_profile_image'),
    path('admin/blogs/delete/', views.delete_blog, name='delete-blog'),
]



