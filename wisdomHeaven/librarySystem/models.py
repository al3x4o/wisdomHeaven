from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL


class User(AbstractUser):
    is_library_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",
        blank=True
    )


class Book(models.Model):
    INVENTORY_CHOICES = [
        ('purchase', 'Purchased'),
        ('donation', 'Donated'),
        ('other', 'Other'),
    ]

    inventory_number = models.CharField(max_length=50, unique=True)
    added_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    edition_type = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    acquisition_method = models.CharField(max_length=20, choices=INVENTORY_CHOICES)
    publisher = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    annotation = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=255)
    attached_file = models.FileField(upload_to='book_files/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.authors}"


class Reader(models.Model):
    national_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.reader.full_name} borrowed {self.book.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
