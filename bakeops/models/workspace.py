from django.conf import settings
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=120)
    legal_name = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, default="United Kingdom")
    currency = models.CharField(max_length=8, default="GBP")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    ROLE_OWNER = "owner"
    ROLE_MANAGER = "manager"
    ROLE_BAKER = "baker"
    ROLE_ANALYST = "analyst"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Owner"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_BAKER, "Baker"),
        (ROLE_ANALYST, "Analyst"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="staff_members",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_staff_profiles",
    )
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_BAKER)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    joined_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["workspace", "full_name"]

    def __str__(self):
        return f"{self.full_name} — {self.workspace}"