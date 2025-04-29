from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from wisdomHeaven.librarySystem.models import Book, Reader, Borrowing, User
from wisdomHeaven.librarySystem.forms import BookForm, ReaderForm, BorrowingForm, RegisterForm, ReturnBookForm, \
    ReviewForm


# Home Page (List all books)
# views.py
from django.db.models import Q
from django.views.generic import ListView
from .models import Book, Borrowing

class IndexView(ListView):
    model = Book
    template_name = "index.html"
    context_object_name = "books"

    def get_queryset(self):
        # Not directly used for available/borrowed split anymore, but keeps default behavior
        query = self.request.GET.get("q", "")
        queryset = Book.objects.all().prefetch_related('borrowings')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(authors__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")

        # Get IDs of currently borrowed books (those with no return date)
        borrowed_books = Borrowing.objects.filter().select_related('book')
        borrowed_book_ids = borrowed_books.values_list('book_id', flat=True)

        # Available books
        available_books = Book.objects.filter(is_available=True).exclude(id__in=borrowed_book_ids)
        if query:
            available_books = available_books.filter(
                Q(title__icontains=query) |
                Q(authors__icontains=query)
            )

        # Filter borrowed books by query as well (if needed)
        if query:
            borrowed_books = borrowed_books.filter(
                Q(book__title__icontains=query) |
                Q(book__authors__icontains=query)
            )

        context['available_books'] = available_books
        context['borrowed_books'] = borrowed_books
        context['search_query'] = query
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['reviews'] = self.object.reviews.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.object
            review.user = request.user
            review.save()
            return redirect('librarySystem:book_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)


# Restrict adding books only to staff
class AddBookView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "add_book.html"
    success_url = reverse_lazy("librarySystem:index")

    def test_func(self):
        return self.request.user.is_staff  # Only staff can add books


class ReturnBookView(LoginRequiredMixin, DeleteView):
    model = Borrowing
    template_name = "return_book.html"
    success_url = reverse_lazy("librarySystem:index")

    def delete(self, request, *args, **kwargs):
        # Get the borrowing record
        borrowing = self.get_object()

        # Update the book's availability before deletion
        book = borrowing.book
        book.is_available = True
        book.save()

        # Add success message
        messages.success(request, f"Book '{book.title}' has been successfully returned")

        # Delete the borrowing record
        return super().delete(request, *args, **kwargs)
# Restrict adding readers only to staff
class AddReaderView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reader
    form_class = ReaderForm
    template_name = "add_reader.html"
    success_url = reverse_lazy("librarySystem:index")

    def test_func(self):
        return self.request.user.is_staff  # Only staff can add readers

class ReaderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reader
    form_class = ReaderForm
    template_name = "edit_reader.html"
    success_url = reverse_lazy("librarySystem:index")

    def test_func(self):
        return self.request.user.is_staff


class ReaderListView(LoginRequiredMixin, ListView):
    model = Reader
    template_name = "reader_list.html"
    context_object_name = "readers"

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = Reader.objects.all()
        if query:
            queryset = queryset.filter(
                Q(full_name__icontains=query) |
                Q(national_id__icontains=query) |
                Q(address__icontains=query) |
                Q(contact_info__icontains=query)
            )
        return queryset


# Restrict borrowing books only to logged-in users
# You can either use a separate view for borrowed books or update the same one

class BorrowBooksView(CreateView):
    model = Borrowing
    form_class = BorrowingForm
    template_name = "borrow_book.html"
    success_url = reverse_lazy("librarySystem:index")

