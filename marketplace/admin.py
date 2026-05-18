from django.contrib import admin
from .models import UserProfile, FlatListing, Message, Booking

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone')
    search_fields = ('user__username', 'location', 'phone')

@admin.register(FlatListing)
class FlatListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'location', 'price', 'size', 'available')
    list_filter = ('available', 'location')
    search_fields = ('title', 'description', 'location')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'sent_at')
    search_fields = ('subject', 'body', 'sender__username', 'receiver__username')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'seller', 'visit_date', 'status')
    list_filter = ('status',)
    search_fields = ('listing__title', 'buyer__username', 'seller__username')
