import jwt

from django.test     import TestCase, Client

from users.models    import User
from posts.models    import Post
from myblog.settings import SECRET_KEY

class PostTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            id       = 1,
            name     = '이름',
            nickname = '닉네임',
            email    = 'test@test.com',
            password = 'test1234!'            
        )
        self.token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        
        Post.objects.create(
            id         = 1,
            user_id    = 1,
            title      = 'title_sample',
            content    = 'content_sample',
        )

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        
    def test_post_create_success(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        data    = {
            'title'   : 'title_sample1',
            'content' : 'content_sample1'
        }
        response = client.post('/posts', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'data' : {
                'title'   : 'title_sample1',
                'content' : 'content_sample1'
            }
        })

    def test_post_create_key_error_fail(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        data    = {
            'content' : 'content_sample1'
        }
        response = client.post('/posts', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'KEY_ERROR'})
    
    def test_post_list_get_success(self):
        client   = Client()
        response = client.get('/posts?limit=10&offset=0', content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_post_list_get_value_error_fail(self):
        client   = Client()
        response = client.get('/posts?limit=xxx&offset=xx', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'VALUE_ERROR'})
        
    def test_post_detail_get_success(self):
        client   = Client()
        response = client.get('/posts/1', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
    def test_post_detail_post_not_found_fail(self):
        client   = Client()
        response = client.get('/posts/2', content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'POST_NOT_FOUND'})

    def test_post_detail_patch_success(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        data    = {
            'title'   : 'title_change',
            'content' : 'content_change'
        }
        response = client.patch('/posts/1', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'UPDATED'})

    def test_post_detail_patch_invalid_post_id_fail(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        data    = {
            'title'   : 'title_change',
            'content' : 'content_change'
        }
        response = client.patch('/posts/2', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'INVALID_POST_ID'})

    def test_post_detail_patch_key_error_fail(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        data    = {
            'content' : 'content_change'
        }
        response = client.patch('/posts/1', data=data, content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_post_detail_delete_success(self):
        client  = Client()
        token   = self.token
        headers = {'HTTP_Authorization': token}
        response = client.delete('/posts/1', content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message': 'post_id 1 is DELETED'})