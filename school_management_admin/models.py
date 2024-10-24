from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from books.models import BookList
# Create your models here.

class User(AbstractUser):
     phone = models.CharField(
        max_length=10, 
        unique=True, 
        blank= True,
        null=True,
        validators=[RegexValidator(
            regex=r"^\d{10}$", 
            message="Phone number must be 10 digits only."
        )]
     )
     is_librarian = models.BooleanField(default=False)
     
     def __str__(self):
         return self.username
     



class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class_name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_title = models.ForeignKey(BookList, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student}_{self.book_title}"

class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    given_book = models.ForeignKey(LibraryHistory, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending')])

    def __str__(self):
        return f"{self.student.name} - {self.amount} - {self.status}"



