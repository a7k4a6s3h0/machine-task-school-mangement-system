from django.urls import path
from . import views

urlpatterns = [
     path('', views.LandingPage.as_view(), name='index'),
     path('login', views.UserLoginView.as_view(), name='login'),
     path('logout', views.UserLogoutView.as_view(), name='logout'),
     path('create_ad', views.CreateAdministratorView.as_view(), name='create_ad'),
     path('administrators', views.AdministatorManagementView.as_view(), name='administrators'),
     path('edit-administrators/<int:pk>', views.EditAdministatorView.as_view(), name='edit-administrators'),
     path('delete-administrators/<int:pk>', views.DeleteAdministatorView.as_view(), name='delete-administrators'),
     path('create_student', views.CreateStudentView.as_view(), name='create_student'),
     path('students', views.StudentManagementView.as_view(), name='students'),
     path('edit-students/<int:pk>', views.EditStudentsView.as_view(), name='edit-students'),
     path('delete-students/<int:pk>', views.DeleteStudentsView.as_view(), name='delete-students'),
     path('give_book', views.GiveBookView.as_view(), name='give_book'),
     path('libary_history', views.LibarayManagementView.as_view(), name='libary_history'),
     path('edit-library-history/<int:pk>', views.EditLibarayHistoryView.as_view(), name='edit-library-history'),
     path('delete-library-history/<int:pk>', views.DeleteLibarayHistoryView.as_view(), name='delete-library-history'),

     path('add_fee_history', views.AddPaymentHistoryView.as_view(), name='add_fee_history'),
     path('edit-fee-history/<int:pk>', views.EditPaymentHistoryView.as_view(), name='edit-fee-history'),

     # path('create_ad', views.create_administrators, name='create_ad'),
     # path('profile', views.profiles, name='profile'),

]
