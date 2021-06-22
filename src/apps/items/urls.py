from django.urls import path
from .views import ListItemView, AddItemView

urlpatterns = [
    path('', ListItemView.as_view()),
    path('add', AddItemView.as_view()),
    path('save', AddItemView.as_view()),
]
