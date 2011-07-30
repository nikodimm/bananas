from django.db import models
from django.contrib.auth.models import User

# activate livesettings
from website import config 


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)

