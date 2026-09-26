from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from bookings.models import Space


class Command(BaseCommand):
    help = "Seed demo spaces for the booking site"

    def handle(self, *args, **options):
        demo_spaces = [
            {
                "name": "The Loft",
                "space_type": "event",
                "description": "A sunlit event hall with exposed beams, ideal for launches, workshops, and mixers up to 80 people.",
                "capacity": 80,
                "price_per_hour": 2500,
                "amenities": "Wifi, PA system, Projector, Kitchenette, Street parking",
                "image_name": "loft.png",
            },
            {
                "name": "Birch Room",
                "space_type": "meeting",
                "description": "A quiet meeting room with a whiteboard wall, good for interviews and small team syncs.",
                "capacity": 6,
                "price_per_hour": 400,
                "amenities": "Wifi, Whiteboard, TV screen, Coffee",
                "image_name": "birch.png",
            },
            {
                "name": "Cedar Room",
                "space_type": "meeting",
                "description": "Our largest meeting room, with a video conferencing setup for hybrid teams.",
                "capacity": 12,
                "price_per_hour": 700,
                "amenities": "Wifi, Video conferencing, Whiteboard, Coffee",
                "image_name": "cedar.png",
            },
            {
                "name": "Hot Desk — Window Row",
                "space_type": "desk",
                "description": "Daily hot desk access along our window row, with natural light and standing-desk options.",
                "capacity": 1,
                "price_per_hour": 100,
                "amenities": "Wifi, Standing desk, Locker",
                "image_name": "hotdesk.png",
            },
            {
                "name": "Private Office 4A",
                "space_type": "private",
                "description": "A lockable private office for small teams, with dedicated storage and a door that closes.",
                "capacity": 4,
                "price_per_hour": 900,
                "amenities": "Wifi, Lockable door, Storage, Whiteboard",
                "image_name": "private.png",
            },
        ]
        created = 0
        for data in demo_spaces:
            image_name = data.pop("image_name", None)
            space, was_created = Space.objects.get_or_create(name=data["name"], defaults=data)
            if was_created:
                created += 1
            # Attach the seed photo whenever the space doesn't already have one
            if image_name and not space.image:
                seed_path = Path(settings.BASE_DIR) / "seed_images" / image_name
                if seed_path.exists():
                    with open(seed_path, "rb") as f:
                        space.image.save(image_name, File(f), save=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new space(s)."))
