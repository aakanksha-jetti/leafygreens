from django.db import models
from home.models import veggies

class CartItem(models.Model):
    product = models.ForeignKey(veggies, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add other fields as needed (e.g., size, color, etc.)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
