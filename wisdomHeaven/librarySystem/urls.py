from django.urls import path

from . import views
from .views import RegisterView, CustomLoginView, CustomLogoutView, BorrowBooksView, ReturnBookView, ReaderUpdateView, \
    ReaderListView

app_name = 'librarySystem'

urlpatterns = [
    # Homepage (index view)
    path('', views.IndexView.as_view(), name='index'),

    # Add new book view
    path('add-book/', views.AddBookView.as_view(), name='add_book'),
    path('add-reader/', views.AddReaderView.as_view(), name='add_reader'),
path("readers/", ReaderListView.as_view(), name="reader_list"),
path("reader/<int:pk>/edit/", ReaderUpdateView.as_view(), name="edit_reader"),

    # Book details view
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path("return/<int:pk>/", ReturnBookView.as_view(), name="return_book"),

    path("borrow/", BorrowBooksView.as_view(), name="borrow_book"),

    path("register/", RegisterView.as_view(), name='register'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name='logout'),
    # Other URL patterns (if needed)
    # path('edit/<int:id>/', views.edit_book, name='edit_book'),
    # path('delete/<int:id>/', views.delete_book, name='delete_book'),
]
