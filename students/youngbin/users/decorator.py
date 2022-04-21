import jwt
from django.conf import settings
from my_settings import ALGORITHM
from .models     import User
from django.http import JsonResponse


#wrapper가 감싸는 변수 자체가 클래스.데코레이터(메소드), 데코레이터에 self나 request등을 줄 수 있다.

def access_token_check(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token,settings.SECRET_KEY,ALGORITHM)
            request.user = User.get.objects(id = payload['id'])

            return func(self,request,*args,**kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'invalid_user'}, status=401)
        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'invalid_signature'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message' : 'invalid_payload'}, status=401)

    return wrapper



        