from django.db import models
from users.models import User
from core.models import TimeStampModel
from users.models import User

class Posting(TimeStampModel):
    author  = models.ForeignKey(User,on_delete=models.CASCADE)
    text    = models.TextField(max_length=500)

    class Meta:
        db_table = 'postings'
    
class Image(TimeStampModel):
    posting   = models.ForeignKey(Posting,on_delete=models.CASCADE)
    image_url = models.TextField()

    class Meta:
        db_table = 'images'
