from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Task(models.Model):
    user = models.ForeignKey('User', related_name="tasks", on_delete = models.CASCADE)
    body = models.CharField(max_length=128)
    done = models.BooleanField(default=False)
    timestamp = models.DateTimeField( auto_now_add= True)

    def __str__(self):
        return f"{self.user.username}: {self.body}"