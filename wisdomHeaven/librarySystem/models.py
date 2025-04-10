from datetime import date

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_library_staff = models.BooleanField(default=False)

    # Fix the related_name clashes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",  # Change this from 'user_set' to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",  # Change this from 'user_set' to avoid conflict
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
    authors = models.CharField(max_length=255)  # You can create a separate Author model if needed
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
    national_id = models.CharField(max_length=10, unique=True)  # Equivalent of EGN in Bulgaria
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.reader.full_name} borrowed {self.book.title}"

    def save(self, *args, **kwargs):
        # Update book availability based on borrow and return dates
        if self.return_date and self.return_date <= date.today():
            self.book.is_available = True
        else:
            self.book.is_available = False

        super().save(*args, **kwargs)
        self.book.save()





