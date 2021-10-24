from django.db    import models

from core.models  import TimeStampModel
from users.models import User

class Post(TimeStampModel):
    title   = models.CharField(max_length=100)
    content = models.TextField()
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'