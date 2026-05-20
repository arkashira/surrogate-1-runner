from django.db import models
from django.core.validators import MinValueValidator


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="orders")
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product_description = models.TextField()

    def __str__(self) -> str:
        return f"Order {self.id} – {self.brand.name} → {self.manufacturer.name}"