import jwt
from django.conf import settings
from my_settings import ALGORITHM
from users.models    import User
from django.http import JsonResponse


#wrapper가 감싸는 변수 자체가 클래스.데코레이터(메소드), 데코레이터에 self나 request등을 줄 수 있다.

def access_token_check(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY,ALGORITHM)
            
            #함수(func)에 유저객체를 담아보내기 위한 것
            self.user = User.objects.get(id = payload['id'])

            return func(self,request,*args,**kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'invalid_user'}, status=401)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'Expired_Signature'}, status=401)
            #exp값이 만료되었을 때(exp에 적힌 값이 현재시간 이후일 때)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'invalid_payload'}, status=401)
            #유효성 검사에 실패하여 토큰을 디코딩 할 수 없을 때, 즉 토큰 자체가 빈 문자열이거나 header혹은 payload가 손상되었을 때 발생, 혹은 시크릿키나 알고리즘이 다를 경우 발생

        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'invalid_signature'}, status=401)
            #토큰의 서명이 일부로 제공된 서명과 일치하지 않을 때 발생 > 걍 조금이라도 맛탱이가면 최종적으로 발생하는 듯 함

    return wrapper