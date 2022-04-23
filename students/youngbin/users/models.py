from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    follow = models.ManyToManyField('self',through='Follow',symmetrical=False)

    class Meta:
        db_table='users'

class Follow(models.Model): 
    follow_from = models.ForeignKey('User',on_delete=models.CASCADE,related_name='follow_from')
    follow_to = models.ForeignKey('User',on_delete=models.CASCADE,related_name='follow_to')
    #related_name이 같거나 설정해주지 않으면(즉 default로 같아지면), 에러가 발생함

    class Meta:
        db_table='follows'
    
#follow기능 참고 블로그
#https://maximeluceyl.tistory.com/42