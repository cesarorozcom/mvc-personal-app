from django.db import models


class MovementImport(models.Model):
    status = models.CharField(max_length=32, default="queued")
    image_key = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImportedMovementProposal(models.Model):
    movement_import = models.ForeignKey(MovementImport, on_delete=models.CASCADE, related_name="proposals")
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True, default="")
    requires_review = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    duplicate_reason = models.TextField(blank=True, default="")
    confirmed = models.BooleanField(default=False)
    discarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
