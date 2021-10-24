import json, re, jwt, bcrypt
from json.decoder import JSONDecodeError

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            name     = data['name']
            nickname = data['nickname']
            email    = data['email']
            password = data['password']

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'message': 'ERROR_ID_ALREADY_EXIST'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'ERROR_EMAIL_ALREADY_EXIST'}, status=400)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=404)
            
            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=404)

            User.objects.create(
                name     = name,
                nickname = nickname,
                email    = email,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=401)
            
            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'token':token}, status=200)
                
            return JsonResponse({'message': 'INVALID_USER_PASSWORD'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'})

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)