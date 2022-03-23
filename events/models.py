from django.db import models

from accounts.models import User


class Activity(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.short_name = self.name[:3].upper()

        super().save(*args, **kwargs)


class Event(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    activity_id = models.ForeignKey(Activity, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_stop = models.DateField()
    confirmed = models.BooleanField(default=False)
    changed_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Diary(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.PROTECT)
    displayed = models.BooleanField(default=False)
    comment = models.TextField(blank=True)