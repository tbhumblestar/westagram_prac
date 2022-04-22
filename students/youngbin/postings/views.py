from django.shortcuts import render
from django.http            import JsonResponse
from django.views           import View
from .models                import User
from core.decorators        import access_token_check
# Create your views here.

class PostingView(View):
    @access_token_check
    def post(self,request):
        
        user = self.user
                
        return JsonResponse({'user_email':user.email}, status=201)

