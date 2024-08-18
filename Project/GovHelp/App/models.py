from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Query(models.Model):
    PENDING = "PeQ"
    APPROVED = "ApQ"
    ADDRESSED = "AdQ"
    STATUS_CHOICES = [
        (PENDING, "Pending Query"),
        (APPROVED, "Approved Query"),
        (ADDRESSED, "Addressed Query"),
    ]

    Title = models.CharField(max_length=150)
    Description = models.TextField(null=True, default="No Description Available")
    Location = models.CharField(max_length=200)
    Status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=PENDING)
    Created = models.DateTimeField(auto_now_add=True)
    Posted_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
