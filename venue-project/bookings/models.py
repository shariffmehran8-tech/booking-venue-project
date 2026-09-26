from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Space(models.Model):
    SPACE_TYPES = [
        ("desk", "Hot Desk"),
        ("meeting", "Meeting Room"),
        ("event", "Event Hall"),
        ("private", "Private Office"),
    ]

    name = models.CharField(max_length=120)
    space_type = models.CharField(max_length=20, choices=SPACE_TYPES, default="meeting")
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=1)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="spaces/", blank=True, null=True)
    amenities = models.CharField(
        max_length=255, blank=True,
        help_text="Comma-separated, e.g. Wifi, Projector, Whiteboard"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def amenity_list(self):
        return [a.strip() for a in self.amenities.split(",") if a.strip()]


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.space.name} — {self.date} {self.start_time}-{self.end_time}"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        if self.space_id and self.date and self.start_time and self.end_time:
            overlapping = Booking.objects.filter(
                space=self.space,
                date=self.date,
                status__in=["pending", "confirmed"],
            ).exclude(pk=self.pk).filter(
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            )
            if overlapping.exists():
                raise ValidationError("This space is already booked for part of that time range.")

    def total_price(self):
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        hours = (end - start).seconds / 3600
        return round(hours * float(self.space.price_per_hour), 2)
