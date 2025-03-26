from django.urls import path
from . import views

app_name = 'librarySystem'

urlpatterns = [
    # Homepage (index view)
    path('', views.IndexView.as_view(), name='index'),

    # Add new book view
    path('add/', views.AddBookView.as_view(), name='add_book'),

    # Book details view
    path('book/<int:id>/', views.BookDetailView.as_view(), name='book_detail'),

    # Other URL patterns (if needed)
    # path('edit/<int:id>/', views.edit_book, name='edit_book'),
    # path('delete/<int:id>/', views.delete_book, name='delete_book'),
]
