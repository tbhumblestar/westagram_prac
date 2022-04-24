from django.db import models
from core.models import TimeStampModel
# Create your models here.

class User(TimeStampModel):
    email          = models.EmailField(max_length=50)
    name           = models.CharField(max_length=200)
    password       = models.CharField(max_length=30)
    stage          = models.IntegerField()

class Store(TimeStampModel):
    name           = models.CharField(max_length=200)
    category       = models.CharField(max_length=30) #fix : choicefield?
    destination    = models.CharField(max_length=30) #fix : choicefield?
    price          = models.CharField(max_length=30) #fix : choicefield?
    
    description    = models.TextField()

    class Meta:
        db_table   = 'stores'

class Image(TimeStampModel):
    store          = models.ForeignKey('Store',on_delete=models.CASCADE,)
    image_url      = models.CharField(max_length = 200)

    class Meta:
        db_table   = 'images'

class Relation(TimeStampModel):
    user           = models.ForeignKey('User',on_delete=models.CASCADE)
    store          = models.ForeignKey('Store',on_delete=models.CASCADE)
    score          = models.DecimalField(max_digits=4,decimal_places=3)
    like_or_height = models.CharField(max_length=30)
    #Like or Heigth

    class Meta:
        db_table    = 'relation'
