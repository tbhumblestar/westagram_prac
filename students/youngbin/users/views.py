import json, bcrypt, jwt
from core.decorators import access_token_check


from datetime               import datetime, timedelta
from my_settings            import ALGORITHM
from westagram.settings     import SECRET_KEY
from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from .models                import User, Follow
from .validation            import (
    validate_password,
    validate_email,
    validate_phone_number)



class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body) 

        try:
            entered_email        = data['email']
            entered_password     = data['password']
            entered_name         = data['name']
            entered_phone_number = data['phone_number']

            validated_password = validate_password(entered_password)
            validated_email = validate_email(entered_email)
            validated_phone_number = validate_phone_number(entered_phone_number)
        
            if User.objects.filter(email=entered_email).exists():
                return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)

            encrypted_password = bcrypt.hashpw(validated_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = entered_name,
                password     = encrypted_password,
                email        = validated_email,
                phone_number = validated_phone_number,
            )
            return JsonResponse({'messasge':'user_created'}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except ValidationError as error:
            return JsonResponse({"message": error.messages}, status=409)


class SignInView(View):
    def post(self,request):
        data = json.loads(request.body) 
        try:
            email                 = data['email']
            password              = data['password']
            user                  = User.objects.get(email=email)
            user_saved_db         = user.password
      
            if bcrypt.checkpw(password.encode('utf-8'),user_saved_db.encode('utf-8')):
                
                #jwt 토큰 로직. bcrypt로 패스워드 로직을 먼저 실행하였음(pw가 안맞으면 jwt로직을 실행할 필요가 없으니까!)
                current_time          = datetime.utcnow()
                expiration_time       = timedelta(seconds=30000000)
                token_expiration_time = current_time+expiration_time
                jwt_access_token = jwt.encode({'id':user.id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)            

                return JsonResponse({'messasge':'SUCCESS','JWT_TOKEN':jwt_access_token}, status=200)
            return JsonResponse({"message":"INCORRECT_PASSWORD"},status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"NOT_REGISTERED_EMAIL"},status=401)

class FollowView(View):
    @access_token_check
    def post(self,request):
        data = json.loads(request.body)
        user = self.user
        try:
            follow_to_email = data['follow_to_email']#이메일로 받지 않을까??
            follow_to       = User.objects.get(email = follow_to_email)
            if Follow.objects.filter(follow_from=user,follow_to=follow_to).exists():
                Follow.objects.filter(follow_from=user,follow_to=follow_to).delete()
                return JsonResponse({"message":"팔로우가 취소되었습니다!"},status=201)

            Follow.objects.create(
                follow_from=user,
                follow_to=follow_to,
                )

            return JsonResponse({"message":"팔로우가 등록되었습니다!"},status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"NOT_REGISTERED_EMAIL"},status=401)