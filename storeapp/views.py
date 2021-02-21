from django.shortcuts import render

# Create your views here.

def categories_view(request):
    return render(request, 'storeapp/categories.html')