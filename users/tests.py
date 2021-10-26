import jwt, bcrypt

from django.test     import TestCase, Client

from myblog.settings import SECRET_KEY
from users.models    import User

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            name='정지훈',
            nickname='jung',
            email='jung1@gmail.com',
            password = 'm111111!'
        )
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_sign_up_post_success(self):
        client = Client()
        data   = {
            'name'     : '정우성',
            'nickname' : 'jungjung',
            'email'    : 'jung2@gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{'message':'SUCCESS'})
    
    def test_sign_up_post_duplicated_nickname_fail(self):
        client = Client()
        data   = {
            'name'     : '정우성',
            'nickname' : 'jung',
            'email'    : 'jung2@gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'NICKNAME_ALREADY_EXIST'})

    def test_sign_up_post_duplicated_email_fail(self):
        client = Client()
        data   = {
            'name'     : '정우성',
            'nickname' : 'jungjung',
            'email'    : 'jung1@gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'EMAIL_ALREADY_EXIST'})
    
    def test_sign_up_post_email_validation_fail(self):
        client = Client()
        data   = {
            'name'     : '정우성',
            'nickname' : 'jungjung',
            'email'    : 'jung2gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'message':'INVALID_EMAIL'})

    def test_sign_up_post_password_validation_fail(self):
        client = Client()
        data   = {
            'name'     : '정우성',
            'nickname' : 'jungjung',
            'email'    : 'jung2@gmail.com',
            'password' : '123111111'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'message':'INVALID_PASSWORD'})

    def test_sign_up_post_key_error_fail(self):
        client = Client()
        data   = {
            'nickname' : 'jungjung',
            'email'    : 'jung2@gmail.com',
            'password' : '123111111'
        }
        response = client.post('/users/signup', data=data, content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'KEY_ERROR'})

class LogInTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            id       = 1,
            name     = '정지훈',
            nickname = 'jung',
            email    = 'jung1@gmail.com',
            password = bcrypt.hashpw('m111111!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        self.token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
    
    def tearDown(self):
        User.objects.all().delete()

    def test_log_in_post_success(self):
        client = Client()
        data   = {
            'email'    : 'jung1@gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/login', data=data, content_type='application/json')
        token    = self.token
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'token':token})
    
    def test_log_in_post_invalid_email_fail(self):
        client = Client()
        data   = {
            'email'    : 'jung777@gmail.com',
            'password' : 'm111111!'
        }
        response = client.post('/users/login', data=data, content_type='application/json')
        token    = self.token
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message':'INVALID_EMAIL'})

    def test_log_in_post_invalid_password_fail(self):
        client = Client()
        data   = {
            'email'    : 'jung1@gmail.com',
            'password' : 'wrong!!!'
        }
        response = client.post('/users/login', data=data, content_type='application/json')
        token    = self.token
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message':'INVALID_PASSWORD'})

    def test_log_in_post_key_error_fail(self):
        client = Client()
        data   = {
            'password' : 'm111111!'
        }
        response = client.post('/users/login', data=data, content_type='application/json')
        token    = self.token
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'KEY_ERROR'})