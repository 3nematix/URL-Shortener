from django.utils import timezone
from django.db import models, IntegrityError
from django.utils.crypto import get_random_string


class Link(models.Model):
    full_url = models.URLField()
    short_url = models.URLField(max_length=7, unique=True)
    key = models.CharField(max_length=32, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    date_expires = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=7)
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def new_view(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.short_url:
            while True:
                try:
                    self.short_url = get_random_string(length=7)
                except IntegrityError:
                    continue
                break

        return super().save(*args, **kwargs)
