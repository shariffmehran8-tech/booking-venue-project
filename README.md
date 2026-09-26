# Commons — Venue Booking (Django)

A co-working / event space booking portfolio piece. Customers browse spaces, see
what's already booked, and request a slot. Staff manage everything — spaces,
pricing, bookings, status — through a customized Django admin, no code needed.

## Features

- Space catalog with type filter (desk / meeting room / event hall / private office)
- Space detail page showing upcoming bookings so customers can see availability
- Booking form with server-side double-booking prevention (`Booking.clean()`)
- Auth: signup, login, logout, "My bookings" with cancel
- Custom Django admin: image thumbnails, bulk confirm/cancel actions, live price
  calculation, date-hierarchy browsing, inline editable status/price
- Clean, mobile-first UI, no frontend framework — just Django templates + CSS

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_spaces    # adds 5 demo spaces with photos (from seed_images/)
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site, `/admin/` for staff management.

## Project structure

```
venuebooking/       # project settings, root urls
bookings/           # the app: models, views, forms, admin, templates
  templates/bookings/     # site pages
  templates/registration/ # login/signup
  management/commands/seed_spaces.py
static/css/main.css # single stylesheet, mobile-first
```

## What to extend next

- Payment capture (Razorpay/Stripe) before confirming a booking
- Email notifications on booking confirm/cancel
- A recurring-booking option for regular co-working members
- Calendar-view (not just list) of a space's upcoming bookings
