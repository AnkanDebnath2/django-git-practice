from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('listing/new/', views.listing_create, name='listing_create'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/edit/', views.listing_update, name='listing_update'),
    path('listing/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('search/', views.search_listings, name='search_listings'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('booking/request/<int:pk>/', views.booking_request, name='booking_request'),
    path('bookings/', views.booking_requests, name='booking_requests'),
    path('booking/<int:pk>/<str:action>/', views.booking_action, name='booking_action'),
]
