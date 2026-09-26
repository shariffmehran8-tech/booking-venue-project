from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Space, Booking
from .forms import BookingForm


def space_list(request):
    spaces = Space.objects.filter(is_active=True)
    space_type = request.GET.get("type")
    if space_type:
        spaces = spaces.filter(space_type=space_type)
    return render(request, "bookings/space_list.html", {
        "spaces": spaces,
        "space_types": Space.SPACE_TYPES,
        "selected_type": space_type,
    })


def space_detail(request, pk):
    space = get_object_or_404(Space, pk=pk, is_active=True)
    upcoming = space.bookings.filter(status__in=["pending", "confirmed"]).order_by("date", "start_time")[:10]
    return render(request, "bookings/space_detail.html", {
        "space": space,
        "upcoming_bookings": upcoming,
    })


@login_required
def book_space(request, pk):
    space = get_object_or_404(Space, pk=pk, is_active=True)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.space = space
            booking.user = request.user
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Booking request sent! You'll see it in 'My Bookings'.")
                return redirect("my_bookings")
            except ValidationError as e:
                for err in e.messages:
                    form.add_error(None, err)
    else:
        form = BookingForm()
    return render(request, "bookings/book_space.html", {"space": space, "form": form})


@login_required
def my_bookings(request):
    bookings = request.user.bookings.select_related("space").all()
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == "POST" and booking.status in ["pending", "confirmed"]:
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect("my_bookings")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("space_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
