from django.urls import path
from .views import ListItemView, AddItemView, UpdateItemView, DeleteItemView


app_name = 'items'
urlpatterns = [
    path('', ListItemView.as_view()),
    path('add', AddItemView.as_view(),name='add'),
    path('save', AddItemView.as_view()),
    path('edit/<int:id>', UpdateItemView.as_view()),
    path('update/<int:id>', UpdateItemView.as_view()),
    path('delete/<int:id>', DeleteItemView.as_view()),
]
