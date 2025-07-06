from django import forms
from .models import ProfileImage
from .models import Category
from .models import Blog
from .models import Pages 

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # Limit to 5MB
                raise forms.ValidationError("Image file too large (max 5MB).")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Only JPEG or PNG images are allowed.")
        return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Category Description'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'id':'title','class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'slug': forms.TextInput(attrs={'id':'slug','class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400','readonly': 'readonly'}),
            'category': forms.Select(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'image': forms.FileInput(attrs={'class':'w-full border border-gray-300 rounded-md px-4 py-2 bg-white file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),           
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'}),
        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Pages
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'title',
                'class': 'mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'slug': forms.TextInput(attrs={
                'id': 'slug',
                'class': 'mt-1 block w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-gray-500',
                'readonly': 'readonly'
            }),
            'image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full p-2 border border-gray-300 rounded-md'
            }),
            'status': forms.Select(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full p-2 border border-gray-300 rounded-md'
            }),
        }

