from django.views.generic import TemplateView, ListView, DetailView, CreateView

from django.urls import reverse_lazy
from wisdomHeaven.librarySystem.models import Book, Reader, Borrowing
from wisdomHeaven.librarySystem.forms import BookForm, ReaderForm, BorrowingForm


# Home Page (List all books)
class IndexView(ListView):
    model = Book
    paginate_by = 10
    template_name = "index.html"
    context_object_name = "books"


# Book Detail Page
class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"


# Add a new Book
class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "add_book.html"
    success_url = reverse_lazy("index")


# Register a new Reader
class AddReaderView(CreateView):
    model = Reader
    form_class = ReaderForm
    template_name = "add_reader.html"
    success_url = reverse_lazy("index")


# Borrow a Book
class BorrowBookView(CreateView):
    model = Borrowing
    form_class = BorrowingForm
    template_name = "borrow_book.html"
    success_url = reverse_lazy("index")
