from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreferences(models.Model):
  # Links this preference to a specific user
  # OneToOneField ensures each user can only have one preference record
  # CASCADE means if user is deleted, their preferences will also be deleted
  user = models.OneToOneField(to=User, on_delete=models.CASCADE)
  
  # Stores the user's preferred currency
  # max_length=255: Allows long currency formats (e.g., "US Dollar (USD)")
  # blank=True: Field is optional in forms
  # null=True: Field can be NULL in database
  currency = models.CharField(max_length=255, blank=True, null=True)
  
  # String representation of this model
  # Example: "john's preferences"
  def __str__(self):
    return str(self.user) + "'s preferences"
  