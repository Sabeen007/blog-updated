from user.models import Pages

def global_vars(request):
    pages = Pages.objects.filter(status=1)
    return {
        'pages': pages,       
    }
