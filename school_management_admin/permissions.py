from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from urllib.parse import urlparse
from django.contrib import messages

roles_and_permissions = {
    'admin': 'all',  # Admin has full access to all views.
    
    'staff': {
        'allowed_url': [
            'students',                # View student details
            'create_student',          # Create students
            'edit-students',           # Edit students
            'delete-students',         # Delete students
            'libary_history',          # View library records
            'add_fee_history',         # Manage fee history
            'edit-fee-history',        # Edit fee history
            'give_book',               # Manage book borrowing
        ]
    },
    
    'librarian': {
        'allowed_url': [
            'students',                # View student details (view-only)
            'libary_history',          # View library history (view-only)
        ]
    },
}

class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
     def test_func(self):
          user = self.request.user
          
          print("user in RedirectAuthenticatedUserMixin")
          # Step 1: Check if the user is authenticated
          if not user.is_authenticated:
               return True

          # If no matching role or permission is found, deny access
          return False

     def handle_no_permission(self):
          # Redirect the user to login page if not authenticated, otherwise to 'students' page if permission is denied
          return redirect(reverse_lazy('students'))  # Redirect to the 'students' page if permission is denied
  
    

class RedirectNotAuthenticatedUserMixin(UserPassesTestMixin):
     
     def test_func(self):
          user = self.request.user
          print("user in RedirectNotAuthenticatedUserMixin", user.username)


          # Step 1: Check if the user is authenticated
          if not user.is_authenticated:
               return False  # User is not authenticated; will be redirected in handle_no_permission
          
          # Step 2: Check the role and allowed URLs
          role_checks = [
               ('admin', user.is_superuser), 
               ('staff', user.is_staff), 
               ('librarian', getattr(user, 'is_librarian', False))  # Using getattr for custom field `is_librarian`
          ]
          
          for role, has_role in role_checks:
               if has_role:  # If user belongs to this role
                    
                    if role in roles_and_permissions:
                         if roles_and_permissions[role] == 'all':  # Admin has full access
                              print(f'{user.username} is {role}')
                              return True
                         
                         # Step 3: Check if the requested URL is in allowed URLs for the role
                         allowed_urls = roles_and_permissions[role].get('allowed_url', [])
                         if self.request.resolver_match.url_name in allowed_urls:
                              print(f'{user.username} is {role}')
                              return True

          # If no matching role or permission is found, deny access
          return False
     
     def handle_no_permission(self):

          # Get the previous URL (referrer)
          previous_url = self.request.META.get('HTTP_REFERER', None)  # Previous URL or None if not present
          if previous_url:
               # Parse the previous URL to get the path (e.g., "/students" or "/book/books")
               parsed_url = urlparse(previous_url)
               # Split the path and take the first or second part
               url_path_segments = parsed_url.path.strip('/').split('/')
               if url_path_segments:
                    relevant_part = url_path_segments[0]  # You can adjust this if you want more than the first part
                    print(f'Relevant part of the previous URL: {relevant_part}')
               else:
                    relevant_part = None
          else:
               relevant_part = None
          
          print(f'Previous URL: {previous_url}, Relevant segment: {relevant_part}')  # For debugging/logging purposes
          
          # Get the current URL kwargs
          current_kwargs = self.request.resolver_match.kwargs
          print(f'Current URL kwargs: {current_kwargs}')  # Log the kwargs (if any)

          if relevant_part is not None and current_kwargs is not None:
                    
               # If there are URL kwargs and a relevant part in the previous URL, redirect to the relevant page
               print('Redirecting with kwargs')
               messages.error(self.request, 'You do not have permission to access this page.')  # Provide error message
               return redirect(reverse_lazy(relevant_part, kwargs=current_kwargs))  # Use actual kwargs
               
          else:
               print('Redirecting without kwargs')
               messages.error(self.request, 'You do not have permission to access this page.')  # Provide error message
               return redirect(reverse_lazy(relevant_part))
