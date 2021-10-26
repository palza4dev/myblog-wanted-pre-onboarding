import json
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from posts.models import Post
from users.utils  import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            Post.objects.create(
                user_id = user.id,
                title   = title,
                content = content
            )
            return JsonResponse({'data': data}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    
    def get(self, request):
        try:
            limit  = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

            if limit > 10:
                return JsonResponse({'message':'TOO_MUCH_LIMIT'}, status=400)

            posts  = Post.objects.all()[offset:offset+limit]

            result = [{
                'post_id'    : post.id,
                'user'       : post.user.name,
                'title'      : post.title,
                "created_at" : post.created_at,
                "updated_at" : post.updated_at
                } for post in posts]
            return JsonResponse({'count': len(posts), 'data':result}, status=200)

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

class PostDetailView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            data = {
                    'post_id'    : post.id,
                    'user'       : post.user.name,
                    'title'      : post.title,
                    'content'    : post.content,
                    "created_at" : post.created_at,
                    "updated_at" : post.updated_at
                }
            return JsonResponse({'data': data}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message' : 'POST_NOT_FOUND'}, status=404)

    @login_decorator
    @transaction.atomic
    def patch(self, request, post_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            if not Post.objects.filter(id=post_id, user=user).exists():
                return JsonResponse({'message':'INVALID_POST_ID'}, status=404)

            post = Post.objects.get(id=post_id, user=user)

            post.content = content
            post.title   = title
            post.save()
            return JsonResponse({'message':'UPDATED'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, post_id):

        user = request.user

        if not Post.objects.filter(id=post_id, user=user).exists():
            return JsonResponse({'message':'INVALID_POST_ID'}, status=404)

        post = Post.objects.get(id=post_id, user=user)
            
        post.delete()
        return JsonResponse({'message': f'post_id {post_id} is DELETED'}, status=200)