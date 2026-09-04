from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Destination, Trip, TripDestination


# =========================================================
# MAIN PAGES
# =========================================================

def home(request):

    destinations = Destination.objects.all()[:6]

    return render(
        request,
        "travel/home.html",
        {
            "destinations": destinations,
        },
    )


def explore(request):

    destinations = Destination.objects.all()

    return render(
        request,
        "travel/explore.html",
        {
            "destinations": destinations,
        },
    )


def destination_detail(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk,
    )

    return render(
        request,
        "travel/destination_detail.html",
        {
            "destination": destination,
        },
    )


def about(request):

    return render(
        request,
        "travel/about.html",
    )


# =========================================================
# TRAVEL STORIES
# =========================================================

def travel_stories(request):

    destinations = Destination.objects.all()

    return render(
        request,
        "travel/travel_stories.html",
        {
            "destinations": destinations,
        },
    )


# =========================================================
# POPULAR STORIES
# =========================================================

def popular_stories(request):

    destinations = Destination.objects.all()

    return render(
        request,
        "travel/popular_stories.html",
        {
            "destinations": destinations,
        },
    )


# =========================================================
# TRAVEL GUIDE
# =========================================================

def travel_guide(request):

    guides = [
        {
            "title": "Planning Your First Journey",
            "description": (
                "Learn how to choose a destination, "
                "set your dates and create an itinerary "
                "that leaves room for discovery."
            ),
            "category": "PLANNING",
        },
        {
            "title": "Choosing the Right Destination",
            "description": (
                "From peaceful islands to mountain escapes, "
                "find a destination that matches your "
                "travel style."
            ),
            "category": "DESTINATIONS",
        },
        {
            "title": "Building a Better Itinerary",
            "description": (
                "Organise your days without planning "
                "every moment. Leave space for unexpected "
                "places and experiences."
            ),
            "category": "PLANNING",
        },
        {
            "title": "Travel on a Thoughtful Budget",
            "description": (
                "Make your journey more comfortable by "
                "planning accommodation, transport, food "
                "and experiences in advance."
            ),
            "category": "BUDGET",
        },
        {
            "title": "What to Pack for Your Journey",
            "description": (
                "Pack lighter and smarter with essentials "
                "that work across city breaks, island "
                "escapes and mountain adventures."
            ),
            "category": "ESSENTIALS",
        },
        {
            "title": "Making Time for Slow Travel",
            "description": (
                "Stay longer, explore deeper and experience "
                "a destination beyond its most famous sights."
            ),
            "category": "SLOW TRAVEL",
        },
    ]

    return render(
        request,
        "travel/travel_guide.html",
        {
            "guides": guides,
        },
    )


# =========================================================
# AUTHENTICATION
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username",
            "",
        ).strip()

        password = request.POST.get(
            "password",
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            return redirect("home")

        error = "Invalid username or password."

    return render(
        request,
        "travel/login.html",
        {
            "error": error,
        },
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip()

        password = request.POST.get(
            "password",
        )

        confirm_password = request.POST.get(
            "confirm_password",
        )

        # -------------------------------------------------
        # REQUIRED FIELDS
        # -------------------------------------------------

        if not username or not password:

            error = (
                "Please fill in all required fields."
            )

        # -------------------------------------------------
        # USERNAME
        # -------------------------------------------------

        elif User.objects.filter(
            username=username,
        ).exists():

            error = (
                "This username is already taken."
            )

        # -------------------------------------------------
        # PASSWORD
        # -------------------------------------------------

        elif password != confirm_password:

            error = (
                "Passwords do not match."
            )

        # -------------------------------------------------
        # CREATE ACCOUNT
        # -------------------------------------------------

        else:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            login(
                request,
                user,
            )

            return redirect("home")

    return render(
        request,
        "travel/register.html",
        {
            "error": error,
        },
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("home")


# =========================================================
# PLAN A JOURNEY
# =========================================================

@login_required
def plan_trip(request):

    destinations = Destination.objects.all()

    if request.method == "POST":

        trip_name = request.POST.get(
            "trip_name",
        )

        start_date = (
            request.POST.get("start_date")
            or None
        )

        end_date = (
            request.POST.get("end_date")
            or None
        )

        selected_destinations = (
            request.POST.getlist(
                "destinations",
            )
        )

        if trip_name:

            trip = Trip.objects.create(
                user=request.user,
                name=trip_name,
                start_date=start_date,
                end_date=end_date,
            )

            for day_number, destination_id in enumerate(
                selected_destinations,
                start=1,
            ):

                destination = get_object_or_404(
                    Destination,
                    pk=destination_id,
                )

                TripDestination.objects.create(
                    trip=trip,
                    destination=destination,
                    day_number=day_number,
                )

            return redirect(
                "my_trips",
            )

    return render(
        request,
        "travel/plan_trip.html",
        {
            "destinations": destinations,
        },
    )


# =========================================================
# MY TRIPS
# =========================================================

@login_required
def my_trips(request):

    trips = Trip.objects.filter(
        user=request.user,
    ).prefetch_related(
        "places__destination",
    )

    return render(
        request,
        "travel/my_trips.html",
        {
            "trips": trips,
        },
    )


# =========================================================
# TRIP DETAIL
# =========================================================

@login_required
def trip_detail(request, trip_id):

    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            "places__destination",
        ),
        pk=trip_id,
        user=request.user,
    )

    return render(
        request,
        "travel/trip_detail.html",
        {
            "trip": trip,
        },
    )


# =========================================================
# EDIT TRIP
# =========================================================

@login_required
def edit_trip(request, trip_id):

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        user=request.user,
    )

    destinations = Destination.objects.all()

    if request.method == "POST":

        trip_name = request.POST.get(
            "trip_name",
            "",
        ).strip()

        start_date = (
            request.POST.get("start_date")
            or None
        )

        end_date = (
            request.POST.get("end_date")
            or None
        )

        selected_destinations = (
            request.POST.getlist(
                "destinations",
            )
        )

        # -------------------------------------------------
        # VALIDATE TRIP NAME
        # -------------------------------------------------

        if not trip_name:

            return render(
                request,
                "travel/edit_trip.html",
                {
                    "trip": trip,
                    "destinations": destinations,
                    "selected_destinations": trip.places.all(),
                    "error": "Please enter a trip name.",
                },
            )

        # -------------------------------------------------
        # UPDATE TRIP DETAILS
        # -------------------------------------------------

        trip.name = trip_name
        trip.start_date = start_date
        trip.end_date = end_date

        trip.save()

        # -------------------------------------------------
        # UPDATE DESTINATIONS
        # -------------------------------------------------

        trip.places.all().delete()

        for day_number, destination_id in enumerate(
            selected_destinations,
            start=1,
        ):

            destination = get_object_or_404(
                Destination,
                pk=destination_id,
            )

            TripDestination.objects.create(
                trip=trip,
                destination=destination,
                day_number=day_number,
            )

        return redirect(
            "my_trips",
        )

    selected_destinations = trip.places.all()

    return render(
        request,
        "travel/edit_trip.html",
        {
            "trip": trip,
            "destinations": destinations,
            "selected_destinations": selected_destinations,
        },
    )


# =========================================================
# DELETE TRIP
# =========================================================

@login_required
def delete_trip(request, trip_id):

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        user=request.user,
    )

    if request.method == "POST":

        trip.delete()

        return redirect(
            "my_trips",
        )

    return render(
        request,
        "travel/delete_trip.html",
        {
            "trip": trip,
        },
    )

# =========================================================
# TRAVEL STORIES
# =========================================================

def travel_stories(request):

    return render(
        request,
        "travel/travel_stories.html",
    )


# =========================================================
# POPULAR STORIES
# =========================================================

def popular_stories(request):

    return render(
        request,
        "travel/popular_stories.html",
    )


# =========================================================
# TRAVEL GUIDE
# =========================================================

def travel_guide(request):

    destinations = Destination.objects.all()

    return render(
        request,
        "travel/travel_guide.html",
        {
            "destinations": destinations,
        },
    )