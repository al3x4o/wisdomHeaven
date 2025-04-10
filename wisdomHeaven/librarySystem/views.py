from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from wisdomHeaven.librarySystem.models import Book, Reader, Borrowing, User
from wisdomHeaven.librarySystem.forms import BookForm, ReaderForm, BorrowingForm, RegisterForm, ReturnBookForm


# Home Page (List all books)
# views.py
class IndexView(ListView):
    model = Book
    template_name = "index.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_books = Book.objects.all()
        context['available_books'] = [book for book in all_books if book.is_available]
        context['borrowed_books'] = [book for book in all_books if not book.is_available]

        return context


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {
            'username': None} # This removes the help text

# Login View
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    next_page = reverse_lazy('librarySystem:index')

# Logout View
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('librarySystem:index')
# Book Detail Page
class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"


# Restrict adding books only to staff
class AddBookView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "add_book.html"
    success_url = reverse_lazy("librarySystem:index")

    def test_func(self):
        return self.request.user.is_staff  # Only staff can add books

class ReturnBookView(LoginRequiredMixin, UpdateView):
    model = Borrowing
    form_class = ReturnBookForm
    template_name = "return_book.html"
    success_url = reverse_lazy("librarySystem:index")

    def form_valid(self, form):
        # Save the borrowing record and set the return_date to today
        borrowing = form.save(commit=False)
        borrowing.return_date = date.today()  # Set the return date to today automatically
        borrowing.save()

        # After the borrowing record is saved, update the book availability
        borrowing.book.is_available = True  # Mark the book as available
        borrowing.book.save()

        return super().form_valid(form)

# Restrict adding readers only to staff
class AddReaderView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reader
    form_class = ReaderForm
    template_name = "add_reader.html"
    success_url = reverse_lazy("librarySystem:index")

    def test_func(self):
        return self.request.user.is_staff  # Only staff can add readers


# Restrict borrowing books only to logged-in users
# You can either use a separate view for borrowed books or update the same one

class BorrowBooksView(CreateView):
    model = Borrowing
    form_class = BorrowingForm
    template_name = "borrow_book.html"
    success_url = reverse_lazy("librarySystem:index")

