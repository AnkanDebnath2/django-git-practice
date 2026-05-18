from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import (BookingRequestForm, FlatListingForm, MessageForm,
                    ProfileUpdateForm, UserRegistrationForm)
from .models import Booking, FlatListing, Message, UserProfile


def home(request):
    listings = FlatListing.objects.filter(available=True)[:12]
    return render(request, 'marketplace/home.html', {'listings': listings})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to Flatax! Your account is ready.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'marketplace/profile.html', {'form': form})


def listing_detail(request, pk):
    listing = get_object_or_404(FlatListing, pk=pk)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = FlatListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, 'Your flat listing has been published.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = FlatListingForm()
    return render(request, 'marketplace/listing_form.html', {'form': form, 'title': 'Create Listing'})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(FlatListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = FlatListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = FlatListingForm(instance=listing)
    return render(request, 'marketplace/listing_form.html', {'form': form, 'title': 'Edit Listing'})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(FlatListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing removed.')
        return redirect('home')
    return render(request, 'marketplace/listing_delete.html', {'listing': listing})


def search_listings(request):
    qs = FlatListing.objects.filter(available=True)
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_size = request.GET.get('min_size')
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if location:
        qs = qs.filter(location__icontains=location)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)
    if min_size:
        qs = qs.filter(size__gte=min_size)
    return render(request, 'marketplace/search.html', {'listings': qs.distinct(), 'query': query, 'location': location})


@login_required
def inbox(request):
    received = request.user.received_messages.select_related('sender', 'listing')
    return render(request, 'marketplace/inbox.html', {'messages': received})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'marketplace/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def booking_request(request, pk):
    listing = get_object_or_404(FlatListing, pk=pk, available=True)
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.buyer = request.user
            booking.seller = listing.seller
            booking.save()
            messages.success(request, 'Visit request sent to the seller.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = BookingRequestForm()
    return render(request, 'marketplace/booking_form.html', {'form': form, 'listing': listing})


@login_required
def booking_requests(request):
    seller_requests = request.user.received_bookings.select_related('listing', 'buyer')
    buyer_requests = request.user.booking_requests.select_related('listing', 'seller')
    return render(request, 'marketplace/booking_requests.html', {
        'seller_requests': seller_requests,
        'buyer_requests': buyer_requests,
    })


@login_required
def booking_action(request, pk, action):
    booking = get_object_or_404(Booking, pk=pk, seller=request.user)
    if action in ['accept', 'reject']:
        booking.status = 'accepted' if action == 'accept' else 'rejected'
        booking.save()
        messages.success(request, f'Booking {booking.status}.')
    return redirect('booking_requests')
