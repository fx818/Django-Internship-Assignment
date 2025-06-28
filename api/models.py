from django.db import models

# Create your models here.

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=64, unique=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or self.telegram_id
