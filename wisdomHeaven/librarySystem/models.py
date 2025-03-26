from django.db import models


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
    attached_file = models.FileField(upload_to='book_files/', null=True, blank=True)  # Upload field for files

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
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reader.full_name} borrowed {self.book.title}"
