from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from. forms import *
from .models import User
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from django.contrib import messages
from .permissions import RedirectAuthenticatedUserMixin, RedirectNotAuthenticatedUserMixin
# Create your views here.

# def user_login(request):
#      return render(request, 'login.html')

class LandingPage(RedirectAuthenticatedUserMixin, View):
     def get(self, request):
          return render(request, 'landing_page/landing.html')


class UserLoginView(RedirectAuthenticatedUserMixin, FormView):
     form_class = UserLoginForm
     template_name = 'login.html'

     def get_form_kwargs(self) -> dict[str, Any]:
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()
        print(kwargs)
        return kwargs
     
     def validate_rolls(self, roll, user):
          rolls_list = [('admin', user.is_superuser), ('staff', user.is_staff), ('librarian', user.is_librarian)]
          for items in rolls_list:
               if items[0] == roll:
                    return items[1]
          return None

         
     def form_valid(self, form):
          # Fetch form data
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          roll = form.cleaned_data.get('role')
          
          # Authenticate the user
          user = authenticate(username=username, password=password)
          if user is None:
               return self.render_to_response(self.get_context_data(form=form, error='Invalid username or password'))

          # Validate the user role
          result = self.validate_rolls(roll, user)
          print(result, 'results')
          if not result:
               return self.render_to_response(self.get_context_data(form=form, error='You are not authorized to access this page'))
          
          # Log the user in
          login(self.request, user)

          return super().form_valid(form)


     def get_success_url(self) -> str:
          return reverse_lazy('students')

class CreateAdministratorView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = CreateAdministratorForm
     template_name = 'create_administrator.html'

     def get_form_kwargs(self) -> dict[str, Any]:
          kwargs =  super().get_form_kwargs()
          print(kwargs)
          return kwargs

     def form_valid(self, form: Any) -> HttpResponse:
          # If form is valid, save the form data (new user)
          form.save()
          
          # Add a success message after saving the form
          messages.success(self.request, 'New user created successfully')
          
          # Redirect to the success URL
          return super().form_valid(form)
     
     def get_success_url(self) -> str:
          # Redirect to the create_ad URL after a successful form submission
          return reverse_lazy('create_ad')

class UserLogoutView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        logout(request)
        # Redirect to the login page or any other page after logout
        return redirect('/')    
    

class AdministatorManagementView(RedirectNotAuthenticatedUserMixin, TemplateView):
     template_name = 'administator_management.html'
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['administrators'] = User.objects.filter(Q(is_superuser = True) |  (Q(is_staff = True) | Q(is_librarian = True)))
          return context


class EditAdministatorView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = EditAdministratorForm
     template_name = 'edit_administrators.html'
     
     def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the pk from URL
        user = User.objects.get(id=pk)  # Fetch the user
        kwargs['instance'] = user  # Pass the user instance to the form
        return kwargs

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          pk = self.kwargs.get('pk')  
          context['administrator_details'] = User.objects.get(id=pk)
          return context

     def form_valid(self, form):
          form.save()
          messages.success(self.request, 'Administrator updated successfully')
          return super().form_valid(form)

     def get_success_url(self) -> str:
          pk = self.kwargs.get('pk')  # Get the pk from kwargs
          return reverse_lazy('edit-administrators', kwargs={'pk': pk})  # Redirect to the same page

     
class DeleteAdministatorView(RedirectNotAuthenticatedUserMixin, View):
     def get(self, request, pk):
          user = User.objects.get(pk=pk)
          user.delete()
          messages.error(request, 'user deleted sucessfully')
          return redirect('administrators')


class CreateStudentView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = CreateStudentForm
     template_name = 'create_student.html'

     def form_valid(self, form):
         form.save()
         messages.success(self.request, 'Student created successfully')
         return super().form_valid(form)
     
     def get_success_url(self) -> str:
          return reverse_lazy('create_student')
     

class StudentManagementView(RedirectNotAuthenticatedUserMixin, TemplateView):
     template_name = 'students_mangement.html'

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          context['students_details'] = Student.objects.all()
          return context
     

class DeleteStudentsView(RedirectNotAuthenticatedUserMixin, View):
     def get(self, request, pk):
          user = Student.objects.get(pk=pk)
          user.delete()
          messages.error(request, 'user deleted sucessfully')
          return redirect('administrators')     
     


class EditStudentsView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = EditStudentsForm
     template_name = 'edit_students.html'
     
     def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the pk from URL
        user = Student.objects.get(id=pk)  # Fetch the user
        kwargs['instance'] = user  # Pass the user instance to the form
        return kwargs

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          pk = self.kwargs.get('pk')  
          context['student_details'] = Student.objects.get(id=pk)
          return context

     def form_valid(self, form):
          form.save()
          messages.success(self.request, 'Student data updated successfully')
          return super().form_valid(form)

     def get_success_url(self) -> str:
          pk = self.kwargs.get('pk')  # Get the pk from kwargs
          return reverse_lazy('edit-students', kwargs={'pk': pk})  # Redirect to the same page     
     

class GiveBookView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = GiveBookForm
     template_name = 'assign_book.html'
     success_url = reverse_lazy('give_book')

     def form_valid(self, form):
         form.save()
         messages.success(self.request, 'Book assigned successfully')
         return super().form_valid(form)

class LibarayManagementView(RedirectNotAuthenticatedUserMixin, TemplateView):
     template_name = 'library_history.html'   

     def get_context_data(self, **kwargs) -> dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context["history_details"] = LibraryHistory.objects.all().order_by('-created_at')
         return context
       
class EditLibarayHistoryView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = EditLibarayHistoryForm
     template_name = 'edit_libaray_history.html'

     def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the pk from URL
        user = LibraryHistory.objects.get(id=pk)  # Fetch the user
        kwargs['instance'] = user  # Pass the user instance to the form
        return kwargs

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          pk = self.kwargs.get('pk')  
          context['libary_details'] = LibraryHistory.objects.get(id=pk)
          return context
     
     def get_success_url(self) -> str:
          pk = self.kwargs.get('pk')  # Get the pk from kwargs
          return reverse_lazy('edit-library-history', kwargs={'pk': pk})  # Redirect to the same page   

class DeleteLibarayHistoryView(RedirectNotAuthenticatedUserMixin, View):
     def get(self, request, pk):
          libaray_data = LibraryHistory.objects.get(pk=pk)
          fee_data = FeesHistory.objects.get(given_book = libaray_data)
          fee_data.delete()
          libaray_data.delete()
          messages.error(request, 'Libaray data deleted sucessfully')
          return redirect('libary_history')     


class AddPaymentHistoryView(RedirectNotAuthenticatedUserMixin, FormView):
    form_class = AddPaymentHistoryForm
    template_name = 'add_fee_history.html'

    def get(self, request, *args, **kwargs):
        book_id = request.GET.get('book_id')  # Fetching 'book_id' from query params
        if book_id is not None:
            try:
                book_data = LibraryHistory.objects.get(id=book_id)  # Find book based on the id
                fee_data = FeesHistory.objects.get(given_book=book_data)  # Check if a fee history already exists
                return HttpResponseRedirect(reverse_lazy('edit-fee-history', kwargs={'pk': fee_data.id}))  # Redirect to edit if it exists
            except (LibraryHistory.DoesNotExist, FeesHistory.DoesNotExist):
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Payment history added successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_fee_history')

     
class EditPaymentHistoryView(RedirectNotAuthenticatedUserMixin, FormView):
     form_class = EditPaymentHistoryForm
     template_name = 'fees_details.html'

     def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')  # Get the pk from URL
        user = FeesHistory.objects.get(id=pk)  # Fetch the user
        kwargs['instance'] = user  # Pass the user instance to the form
        return kwargs

     def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
          context = super().get_context_data(**kwargs)
          pk = self.kwargs.get('pk')  
          context['fee_details'] = FeesHistory.objects.get(id=pk)
          return context
     
     def form_valid(self, form):
         form.save()
         messages.success(self.request, 'Payment history updated successfully')
         return super().form_valid(form)
     

     def get_success_url(self) -> str:
          pk = self.kwargs.get('pk')  
          return reverse_lazy('edit-fee-history', kwargs={'pk': pk}) 