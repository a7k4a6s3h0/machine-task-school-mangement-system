from django.db import models

# Create your models here.


class BookList(models.Model):
     title = models.CharField(max_length=20)
     author = models.CharField(max_length=100)
     price = models.DecimalField(max_digits=5, decimal_places=2)
     image = models.ImageField(upload_to='images/')
     description = models.CharField(max_length=50, default='No description available')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     is_active = models.BooleanField(default=True)

     def __str__(self) -> str:
          return f"book_{self.title}"
