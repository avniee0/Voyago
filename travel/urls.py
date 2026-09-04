from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # MAIN PAGES
    # =====================================================

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "explore/",
        views.explore,
        name="explore",
    ),

    path(
        "destination/<int:pk>/",
        views.destination_detail,
        name="destination_detail",
    ),

    path(
        "about/",
        views.about,
        name="about",
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),


    # =====================================================
    # TRIPS
    # =====================================================

    path(
        "plan-trip/",
        views.plan_trip,
        name="plan_trip",
    ),

    path(
        "trips/",
        views.my_trips,
        name="my_trips",
    ),

    path(
        "my-trips/<int:trip_id>/",
        views.trip_detail,
        name="trip_detail",
    ),

    path(
        "my-trips/<int:trip_id>/edit/",
        views.edit_trip,
        name="edit_trip",
    ),

    path(
        "my-trips/<int:trip_id>/delete/",
        views.delete_trip,
        name="delete_trip",
    ),


    # =====================================================
    # DISCOVER
    # =====================================================

    path(
        "travel-stories/",
        views.travel_stories,
        name="travel_stories",
    ),

    path(
        "popular-stories/",
        views.popular_stories,
        name="popular_stories",
    ),

    path(
        "travel-guide/",
        views.travel_guide,
        name="travel_guide",
    ),
]