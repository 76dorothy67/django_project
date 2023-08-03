from django.shortcuts import render
from boards.models import Category

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', context={'categories': categories})
