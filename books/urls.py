from django.urls import path
from . import views

urlpatterns = [
    path('add_books', views.CreateBookView.as_view(), name='add_books'),
    path('books', views.BookManagementView.as_view(), name='books'),
    path('edit-book/<int:pk>', views.EditBooksView.as_view(), name='edit-book'),
    path('delete-books/<int:pk>', views.DeleteBookView.as_view(), name='delete-books'),

]
