import json

from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View
from .models                import User
from core.decorators        import access_token_check
from postings.models        import Posting, Image, Comment, Like
from django.core.exceptions import ValidationError
# Create your views here.

class PostingView(View):
    @access_token_check
    def post(self,request):
        data = json.loads(request.body)
        try:
            user            = self.user
            title           = data['title']
            text            = data.get('text',None) #없을 수도 있음

            image_url_list  = data.get('image_url_list',None).split(',') #없을 수도 있음, #문자열을 리스트로 바꿔줘야 함!
            
            Posting.objects.create(
                author  = user,
                title   = title,
                text    = text,
            )

            posting = Posting.objects.last()

            for image_url in image_url_list:
                Image.objects.create(
                    posting   = posting,
                    image_url = image_url,
                )
      
            return JsonResponse({'messasge':'posting_created'}, status=201)
                    
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

    def get(self,request):
        posting_list = []
        for posting in Posting.objects.all():
            image_list = []
            # for image in posting.images.all():
            #     image_list.append(image.image_url)
            posting_list.append({
                'author_email' : posting.author.email,
                'title'        : posting.title,
                'text'         : posting.text,
                'created_time' : posting.created_at,
                'posting_id'   : posting.pk,
                'images'       : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
                'likes_count'  : posting.likes.all().count()
            })

        return JsonResponse({'posting_list':posting_list}, status=200)



class CommentView(View):
    @access_token_check
    def post(self,request,posting_id):
        data = json.loads(request.body)
        try:
            user            = self.user
            text            = data['text']
            
            #만약 json데이터로 posting_id를 받을 경우
            #posting_id      = int(data['posting_id'])
            #json데이터로 posting객체를 잡아올 수 있나?? 안되면 객체를 여기서 잡아주는 수 밖에 없음
            
            posting = Posting.objects.get(id=posting_id)

            Comment.objects.create(
                user    = user,
                text    = text,
                posting = posting,
                #posting_id = posting_id, #이렇게도 할 수 있다.
            )

            return JsonResponse({'messasge':'comment_created'}, status=201)
                    
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

        except Posting.DoesNotExist:
            return JsonResponse({"message":"POSTING_DOES_NOT_EXIST"},status=404)

    def get(self,request,posting_id):#특정 게시글의 comment를 보려고 하는 것임 / 최신순?
        posting = Posting.objects.get(id=posting_id)
        comments_list = [{"user":comment.user.name,"text":comment.text} for comment in posting.comments.all()]
        return JsonResponse({
            "message"       : "success",
            'comments_list' : comments_list
            }, status=200)


class LikeView(View):
    @access_token_check
    def post(self,request,posting_id):
        try:
            user    = self.user
            posting = Posting.objects.get(id=posting_id)

            if Like.objects.filter(user=user,posting=posting).exists():
                Like.objects.filter(user=user,posting=posting).delete()
                return JsonResponse({'messasge':'좋아요 취소!'}, status=201)

            else:
                Like.objects.create(
                    user    = user,
                    posting = posting,
                )
                return JsonResponse({'messasge':'좋아요 성공!'}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except Posting.DoesNotExist:
            return JsonResponse({"message":"POSTING_DOES_NOT_EXIST"},status=404)

    def get(self,request,posting_id):
            try:
                posting    = Posting.objects.get(id=posting_id)
                like_count = posting.likes.all().count()
                
                return JsonResponse({'like_count':like_count}, status=201)

            except Posting.DoesNotExist:
                return JsonResponse({"message":"POSTING_DOES_NOT_EXIST"},status=404)

        


