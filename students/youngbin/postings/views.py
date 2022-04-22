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
            text            = data['text']
            image_url_list  = data['image_url_list']

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
        


                