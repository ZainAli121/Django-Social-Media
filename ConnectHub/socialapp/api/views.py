from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from socialapp.models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST']) # This decorator allows us to use function based views instead of class based views
def getRoutes(request):
    routes = [
        'GET /api',
        # 'GET /api/users',
        # 'GET /api/users/id',
        # 'POST /api/login',
        # 'GET /api/users/profile',
        'GET /api/posts',
        'GET /api/posts/id',
    ]

    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getPosts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) # many = True means we are serializing multiple objects
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getPost(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response({"success": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(['GET'])
def getProfile(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# @api_view(['POST'])
# def createPost(request):
#     data = request.data
#     user = request.user
#     post = Post.objects.create(
#         user=user,
#         body=data['body'],
#     )
#     serializer = PostSerializer(post, many=False)
#     return Response(serializer.data)
