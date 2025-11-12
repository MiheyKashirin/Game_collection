from django.db import models
from django.contrib.auth.models import User




class Game(models.Model):
    STATUS_CHOICES = [
        ('playing', 'Playing'),
        ('completed', 'Completed'),
        ('wishlist', 'Wishlist'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wishlist')
    rating = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.title} ({self.platform})"
