import datetime

from django import forms
from .models import Book, Reader, Borrowing, User, Review


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label="Username",
        help_text=''  # Remove default help text
    )
    email = forms.EmailField(
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text=''  # No help text here either
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Proper hashing
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['is_available']


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = '__all__'
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available books
        self.fields['book'].queryset = Book.objects.filter(is_available=True)

class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("return_date"):
            cleaned_data["return_date"] = datetime.date.today()  # Default to today's date
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
