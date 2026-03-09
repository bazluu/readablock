from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserMeta(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(UserMeta, self).save(*args, **kwargs)
