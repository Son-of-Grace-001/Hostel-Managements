from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path ('', views.home, name='home'),
    path ('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('complaint/', views.complaint, name='complaint'),
    path('bookpass/', views.book_pass, name='pass'),
    path('book_room/', views.book_room, name='book_room'),
    path('fee/', views.hostel_fees, name= 'hostel_fees'),
    path('pay/', views.upload_school_fee_evidence, name= 'payment'),
    #  path('paystack/callback/', views.paystack_callback, name='paystack_callback'),
   
    # Other URL patterns...
]