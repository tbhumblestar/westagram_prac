from django.db import models
from users.models import User
from core.models import TimeStampModel
from users.models import User

class Posting(TimeStampModel):
    author  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='postings')
    title   = models.CharField(max_length=50)
    text    = models.TextField(max_length=500)
    tag     = models.ManyToManyField('Tag',blank=True,related_name='_postings',through='Posting_Tag')
    #postings이름이 겹쳐서 설정해줄 수가 없음 ㅠㅠ
    #posting에서만 blank = true를 줘도, tag를 생성할 때 posting을 지정해주지 않아도 됨 ㅇㅇ

    class Meta:
        db_table = 'postings'


class Image(TimeStampModel):
    posting   = models.ForeignKey(Posting,on_delete=models.CASCADE,related_name='images')
    image_url = models.TextField()

    class Meta:
        db_table = 'images'


class Comment(TimeStampModel):
    posting   = models.ForeignKey(Posting,on_delete=models.CASCADE,related_name='comments')
    user      = models.ForeignKey(User,on_delete=models.CASCADE,related_name='users')
    text      = models.TextField(max_length=500)

    class Meta:
        db_table = 'comments'


class Like(TimeStampModel):
    #진짜 Like에 따라 한행의 데이터를 삭제하는 게 효율적인 걸까?
    user    = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    posting = models.ForeignKey(Posting,on_delete=models.CASCADE,related_name='likes')

class Tag(TimeStampModel):
    tag_name = models.CharField(max_length=20,unique=True)#태그는 유일무이

    class Meta():
        db_table = 'tags'

class Posting_Tag(TimeStampModel):
    posting = models.ForeignKey('Posting',on_delete=models.CASCADE)
    Tag     = models.ForeignKey('Tag',on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Posting_Tags'