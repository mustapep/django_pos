from django.urls import path
from .views import *


app_name = 'items'
urlpatterns = [
    path('', ListItemView.as_view()),
    path('add', AddItemView.as_view(), name='add'),
    path('save', AddItemView.as_view()),
    path('edit/<int:id>', UpdateItemView.as_view()),
    path('update/<int:id>', UpdateItemView.as_view()),
    path('delete/<int:id>', DeleteItemView.as_view()),
    path('categories', ListCategoriesView.as_view()),
    path('categories/add', AddCategoriesView.as_view()),
    path('categories/<int:id>/delete', DeleteCategoriesView.as_view()),
]
