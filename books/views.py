from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from. forms import *
from .models import BookList
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class CreateBookView(FormView):
     form_class = CreateBooksForm
     template_name = 'create_book.html'

     def form_valid(self, form):
         form.save()
         messages.success(self.request, 'book created sucessfully')
         return super().form_valid(form)
     
     def get_success_url(self) -> str:
          return reverse_lazy('add_books')
     
class BookManagementView(TemplateView):
     template_name = 'book_management.html'

     def get_context_data(self, **kwargs) -> dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context["books_details"] = BookList.objects.all() 
         return context


class EditBooksView(FormView):
     form_class = EditBooksForm
     template_name = 'book_details.html'

     def get_form_kwargs(self):
          kwargs = super().get_form_kwargs()
          pk = self.kwargs.get('pk')  # Get the pk from URL
          try:
               book = BookList.objects.get(id=pk)  # Fetch the book instance
          except BookList.DoesNotExist:
               raise Http404("Book not found")  # Handle case where book is not found
          kwargs['instance'] = book  # Pass the book instance to the form
          return kwargs

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          pk = self.kwargs.get('pk')  
          context['book_details'] = BookList.objects.get(id=pk)
          return context

     def form_valid(self, form):
          form.save()
          messages.success(self.request, 'Book updated successfully')
          return super().form_valid(form)
     
     def get_success_url(self):
          # After saving, redirect back to the edit page
          pk = self.kwargs.get('pk')  # Get the pk from kwargs
          return reverse_lazy('edit-book', kwargs={'pk': pk})  # Redirect to the same page


class DeleteBookView(View):
     def get(self, request, pk):
          user = BookList.objects.get(pk=pk)
          user.delete()
          messages.error(request, 'user deleted sucessfully')
          return redirect('books')     