from django.contrib import admin

from .models import (
    Destination,
    Favorite,
    Trip,
    TripDestination,
    Review,
)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "category",
        "best_time",
        "created_at",
    )

    list_filter = (
        "category",
        "country",
    )

    search_fields = (
        "name",
        "country",
        "description",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "destination",
        "created_at",
    )

    search_fields = (
        "user__username",
        "destination__name",
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "name",
        "user__username",
    )


@admin.register(TripDestination)
class TripDestinationAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "destination",
        "day_number",
    )

    list_filter = (
        "day_number",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "destination",
        "user",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
    )

    search_fields = (
        "destination__name",
        "user__username",
        "comment",
    )