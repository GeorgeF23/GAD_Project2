from django.urls import path
from .views import categories_view, category_view

app_name = 'storeapp'

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/<int:category_id>/', category_view, name='view_category')
]