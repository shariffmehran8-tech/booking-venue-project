from django.contrib import admin
from django.utils.html import format_html
from .models import Space, Booking


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("name", "space_type", "capacity", "price_per_hour", "is_active", "thumbnail")
    list_filter = ("space_type", "is_active")
    search_fields = ("name", "description")
    list_editable = ("is_active", "price_per_hour")
    fieldsets = (
        ("Basic Info", {"fields": ("name", "space_type", "description", "image")}),
        ("Capacity & Pricing", {"fields": ("capacity", "price_per_hour")}),
        ("Details", {"fields": ("amenities", "is_active")}),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    thumbnail.short_description = "Preview"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("space", "user", "date", "start_time", "end_time", "status", "price_display")
    list_filter = ("status", "date", "space")
    search_fields = ("space__name", "user__username", "user__email")
    date_hierarchy = "date"
    list_editable = ("status",)
    autocomplete_fields = ("space", "user")
    actions = ["mark_confirmed", "mark_cancelled"]

    def price_display(self, obj):
        return f"₹{obj.total_price()}"
    price_display.short_description = "Total"

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status="confirmed")
        self.message_user(request, f"{updated} booking(s) marked confirmed.")

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} booking(s) marked cancelled.")


admin.site.site_header = "Venue Booking Admin"
admin.site.site_title = "Venue Booking"
admin.site.index_title = "Manage Spaces & Bookings"
