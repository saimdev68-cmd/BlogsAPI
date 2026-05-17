from django.contrib import admin
from .models import CustomUser, Profile


# Inline profile inside user admin panel
class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0


# Custom admin configuration for users
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):

    # Show profile model inside user admin
    inlines = [ProfileInline]

    # Fields visible in admin list page
    list_display = ["email", "username", "is_active", "is_staff"]

    # Add search functionality in admin
    search_fields = ["email", "username"]