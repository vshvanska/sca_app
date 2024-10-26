from django.db import models
from rest_framework.exceptions import ValidationError
from cats.models import Cat


class Mission(models.Model):
    cat = models.ForeignKey(
        Cat, null=True, blank=True, on_delete=models.SET_NULL, related_name="missions"
    )

    @property
    def is_completed(self):
        return all(target.is_completed for target in self.targets.all())

    def delete(self, *args, **kwargs):
        if self.cat:
            raise ValidationError("Assigned to cat mission can't be deleted")
        super().delete(*args, **kwargs)


class Target(models.Model):
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="targets"
    )
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("mission", "name"),)
