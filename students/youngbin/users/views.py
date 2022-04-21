import json, bcrypt, jwt


from datetime               import datetime, timedelta
from my_settings            import ALGORITHM
from westagram.settings     import SECRET_KEY
from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from .models                import User
from .validation            import (
    validate_password,
    validate_email,
    validate_phone_number)

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body) 

        try:
            new_email        = data['email']
            new_password     = data['password']
            new_name         = data['name']
            new_phone_number = data['phone_number']

            validated_password = validate_password(new_password)
            validated_email = validate_email(new_email)
            validated_phone_number = validate_phone_number(new_phone_number)
        
            if User.objects.filter(email=new_email).exists():
                return JsonResponse({"message":"ALREADY_EXISTED_EMAIL"},status=409)

            encrypted_password = bcrypt.hashpw(validated_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = new_name,
                password     = encrypted_password,
                email        = validated_email,
                phone_number = validated_phone_number,
            )
            return JsonResponse({'messasge':'created'}, status=201)

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
      
            current_time          = datetime.utcnow()
            expiration_time       = timedelta(seconds=300)
            token_expiration_time = current_time+expiration_time

            jwt_access_token = jwt.encode({'id':user.id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)            

            if bcrypt.checkpw(password.encode('utf-8'),user_saved_db.encode('utf-8')):
                return JsonResponse({'messasge':'SUCCESS','JWT_TOKEN':jwt_access_token}, status=200)
            return JsonResponse({"message":"INCORRECT_PASSWORD"},status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"NOT_REGISTERED_EMAIL"},status=401)