from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserMeta(models.Model):
    class DailyWordGoal(models.IntegerChoices):
        W140 = 140
        W550 = 550
        W1370 = 1370
        W2740 = 2740

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verified = models.BooleanField(default=False)
    daily_word_goal = models.IntegerField(
        choices=DailyWordGoal.choices,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(UserMeta, self).save(*args, **kwargs)
