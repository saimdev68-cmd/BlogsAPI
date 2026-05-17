from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user model using email for login
class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    

# Profile model connected to user
class Profile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    name = models.CharField(max_length=255)

    # Store profile image
    profile_image = models.ImageField(
        upload_to="profile/",
        default="default.png"
    )

    def __str__(self):
        return self.name