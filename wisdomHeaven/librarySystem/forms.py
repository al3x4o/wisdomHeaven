from django import forms
from .models import Book, Reader, Borrowing


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = '__all__'
