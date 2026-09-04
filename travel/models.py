from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    CATEGORY_CHOICES = [
        ("beach", "Beach"),
        ("mountain", "Mountain"),
        ("city", "City"),
        ("nature", "Nature"),
        ("heritage", "Heritage"),
    ]

    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    image = models.ImageField(
        upload_to="destinations/",
        blank=True,
        null=True
    )
    best_time = models.CharField(max_length=100, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}, {self.country}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "destination")

    def __str__(self):
        return f"{self.user.username} → {self.destination.name}"


class Trip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trips"
    )

    name = models.CharField(max_length=150)

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class TripDestination(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="places"
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="trip_entries"
    )

    day_number = models.PositiveIntegerField(
        default=1
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["day_number"]
        unique_together = ("trip", "destination")

    def __str__(self):
        return (
            f"{self.trip.name} → "
            f"{self.destination.name}"
        )


class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.destination.name} - "
            f"{self.rating}/5"
        )