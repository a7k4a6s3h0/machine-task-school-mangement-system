from typing import Any
from django import forms
from .models import BookList


class CreateBooksForm(forms.ModelForm):
     class Meta:
          model = BookList
          fields = ('title', 'author', 'description', 'price', 'image')
          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
               'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author'}),
               'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
               'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price'}),
               'image': forms.FileInput(attrs={'class': 'form-control'}),
               }  # end of widgets
          labels = {
               'title': 'Title',
               'author': 'Author',
               'description': 'Description',
               'price': 'Price',
               'image': 'Image',
          }

class EditBooksForm(forms.ModelForm):
     class Meta:
          model = BookList
          fields = ('title', 'author', 'description', 'price', 'image')
          widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
               'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author'}),
               'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
               'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter price'}),
               'image': forms.FileInput(attrs={'class': 'form-control'}),
               }  # end of widgets
          labels = {
               'title': 'Title',
               'author': 'Author',
               'description': 'Description',
               'price': 'Price',
               'image': 'Image',
          }

