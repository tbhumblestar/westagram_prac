import json

from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View
from .models                import User
from core.decorators        import access_token_check
from postings.models        import Posting, Image
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
      
            return JsonResponse({'messasge':'created'}, status=201)
                    
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

    def get(self,request):
        posting_list = []
        for posting in Posting.objects.all():
            image_list = []
            # for image in posting.images.all():
            #     image_list.append(image.image_url)
            posting_list.append({
                'author_email'       : posting.author.email,
                'title'        : posting.title,
                'text'         : posting.text,
                'created_time' : posting.created_at,
                'pk'           : posting.pk,
                'images'       : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
            })

        return JsonResponse({'posting_list':posting_list}, status=200)

        


                