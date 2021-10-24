from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name     = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    email    = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'users'