from typing import Any
from django import forms
import re
from .models import User, Student , LibraryHistory, FeesHistory
from books.models import *

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        label='Username', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'id': "username", 
                'name': "username", 
                'placeholder': "Enter username", 
                'required': True
            }
        )
    )
    password = forms.CharField(
        max_length=100, 
        label='Password', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'id': "password", 
                'name': "password", 
                'placeholder': "Enter password", 
                'required': True
            }
        )
    )
    role = forms.ChoiceField(
        label='Select Role',
        choices=[
            ('admin', 'Admin'),
            ('staff', 'Office Staff'),
            ('librarian', 'Librarian'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-control', 
                'id': 'role', 
                'name': 'role', 
                'required': True
            }
        )
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        role = cleaned_data.get('role')

        if role is None:
            raise forms.ValidationError('Please select a role.')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Invalid username.')

        if not re.match(r'^[a-zA-Z0-9_]+$', password):
            raise forms.ValidationError('Invalid password.')

        return cleaned_data


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()  # Reference your custom User model

class CreateAdministratorForm(forms.ModelForm):
     ROLE_CHOICES = [
          ('admin', 'Admin'),
          ('staff', 'Office Staff'),
          ('librarian', 'Librarian'),
     ]

     role = forms.ChoiceField(
          choices=ROLE_CHOICES,
          widget=forms.Select(
               attrs={
                    'class': 'form-control',
                    'id': 'role',
                    'name': 'role',
                    'required': True
               }
          )
     )

     class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'username',
                    'name': 'username',
                    'placeholder': 'Enter username',
                    'required': True
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'id': 'email',
                    'name': 'email',
                    'placeholder': 'email@gmail.com',
                    'required': True
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'id': 'password',
                    'name': 'password',
                    'placeholder': '******',
                    'required': True
                }
            ),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'role': 'Role'
        }
        error_messages = {
            'username': {
                'required': 'Please enter a username.'
            },
            'email': {
                'required': 'Please enter an email.'
            },
            'password': {
                'required': 'Please enter a password.'
            },
            'role': {
                'required': 'Please select a role.'
            }
        }

     def clean(self) -> dict:
          cleaned_data = super().clean()
          username = cleaned_data.get('username')
          email = cleaned_data.get('email')
          password = cleaned_data.get('password')
          role = cleaned_data.get('role')

          if role is None:
               raise ValidationError('Please select a role.')

          if username and not re.match(r'^[a-zA-Z0-9_]+$', username):
               raise ValidationError('Invalid username. Only letters, numbers, and underscores are allowed.')

          if email and not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
               raise ValidationError("Email address is not valid")

          if password and not re.match(r'^[a-zA-Z0-9_]+$', password):
               raise ValidationError('Invalid password. Only letters, numbers, and underscores are allowed.')

          return cleaned_data

     def save(self, commit: bool = True) -> User:
          obj = super().save(commit=False)  # Avoid saving immediately

          # Set the password properly
          obj.set_password(self.cleaned_data['password'])

          # Set user roles based on selected role
          role = self.cleaned_data['role']
          if role == 'admin':
               obj.is_superuser = True
               obj.is_staff = True
               obj.is_librarian = True
          elif role == 'staff':
               obj.is_superuser = False
               obj.is_staff = True
               obj.is_librarian = False
          elif role == 'librarian':
               obj.is_superuser = False
               obj.is_staff = False
               obj.is_librarian = True

          if commit:
               obj.save()  # Save the user if commit is True

          return obj

class EditAdministratorForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Office Staff'),
        ('librarian', 'Librarian'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'role',
                'name': 'role',
                'required': True
            }
        )
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'name': 'password',
                'placeholder': 'Leave blank to keep current password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username',
                    'required': True
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'email@example.com',
                    'required': True
                }
            ),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'role': 'Role'
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_]+$', password):
            raise ValidationError('Invalid password. Only letters, numbers, and underscores are allowed.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Invalid username. Only letters, numbers, and underscores are allowed.')

        if email and not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
            raise ValidationError("Invalid email address")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Set the password only if a new password was entered
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        # Update roles based on the selected role
        role = self.cleaned_data['role']
        user.is_superuser = False
        user.is_staff = False
        user.is_librarian = False

        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
            user.is_librarian = True
        elif role == 'staff':
            user.is_superuser = False
            user.is_staff = True
            user.is_librarian = False
        elif role == 'librarian':
            user.is_superuser = False
            user.is_staff = False
            user.is_librarian = True

        if commit:
            user.save()

        return user
    

class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'age', 'class_name')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'student_name', 
                'placeholder': 'Enter student name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'student_age', 
                'placeholder': 'Enter student age'
            }),
            'class_name': forms.TextInput(attrs={  # Changed to Select widget
                'class': 'form-control', 
                'id': 'student_classname',
                'placeholder': 'Enter class name'
            })
        }
        labels = {
            'name': 'Student Name',
            'age': 'Age',
            'class_name': 'Class Name'
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 3 or age > 100): 
            raise forms.ValidationError("Please enter a valid age between 3 and 100.")
        return age
                                                                           
class EditStudentsForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'name': 'password',
                'placeholder': 'Leave blank to keep current password'
            }
        )
    )

    class Meta:
        model = Student
        fields = ('name', 'age', 'password', 'class_name')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter name',
                    'required': True
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter age',
                    'required': True
                }
            ),
            'class_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter class name',
                    'required': True
                }
            ),
        }
        labels = {
            'name': 'Name',
            'age': 'Age',
            'class_name': 'Class Name',
            'password': 'Password',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_]+$', password):
            raise ValidationError('Invalid password. Only letters, numbers, and underscores are allowed.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('name')
        age = cleaned_data.get('age')

        # Validate age range
        if age and (age < 3 or age > 100):
            self.add_error('age', "Please enter a valid age between 3 and 100.")

        # Validate name with regex
        if username and not re.match(r'^[a-zA-Z0-9_]+$', username):
            self.add_error('name', 'Invalid username. Only letters, numbers, and underscores are allowed.')

        return cleaned_data
    


class GiveBookForm(forms.ModelForm):
    class Meta:
        model = LibraryHistory
        fields = ('student', 'book_title', 'borrowed_date', 'return_date', 'status')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book_title': forms.Select(attrs={'class': 'form-control'}),
            'borrowed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student': 'Student',
            'book_title': 'Book Title',
            'borrowed_date': 'Borrowed Date',
            'return_date': 'Return Date',
            'status': 'Status',
        }

class EditLibarayHistoryForm(forms.ModelForm):

    class Meta:
        model = LibraryHistory
        fields = ('student', 'book_title', 'borrowed_date', 'return_date', 'status')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book_title': forms.Select(attrs={'class': 'form-control'}),
            'borrowed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student': 'Student',
            'book_title': 'Book Title',
            'borrowed_date': 'Borrowed Date',
            'return_date': 'Return Date',
            'status': 'Status',
        }

class AddPaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = FeesHistory
        fields = ['student', 'given_book', 'payment_date', 'amount', 'remarks', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'given_book': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for book selection
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any remarks'}),
            'status': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for status
        }


class EditPaymentHistoryForm(forms.ModelForm):

    class Meta:
        model = FeesHistory
        fields = ['student', 'given_book', 'payment_date', 'amount', 'remarks', 'status']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any remarks'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'given_book': forms.Select(attrs={'class': 'form-control'}),
        }