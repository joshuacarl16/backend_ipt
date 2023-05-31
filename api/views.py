from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, TopicSerializer, CategorySerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Category, Topic, Comment, User

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if user.password == password:
            return Response({'status': 'Username not found'},status=200)
    except User.DoesNotExist:
        return Response({'status': 'Username not found'}, status=400)

    
    return Response({'status': 'Invalid password'}, status=401)


@api_view(['GET'])
@csrf_exempt
def users_list(request, username= ""):
   users = User.objects.all()
   serializer = UserSerializer(users, many=True)
   return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def get_username(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=404)

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def addCategory(request):
    data = request.data
    userId = data['userId']
    user = User.objects.get(pk=userId)
    category = Category.objects.create(
        categoryId = data['categoryId'],
        categoryName=data['categoryName'],
        userId=user,
    )
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def viewCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# TOPICS
@api_view(['GET'])
def viewTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewTopic(request, pk):
    topics = Topic.objects.get(topicId=pk)
    serializer = TopicSerializer(topics, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addTopic(request):
    data = request.data
    category_id = data['categoryId']
    user_id = data['userId']
    category = Category.objects.filter(pk=category_id).first()
    user = User.objects.get(pk=user_id)
    topics = Topic.objects.create(
        topicId=data['topicId'],
        title=data['title'],
        description=data['description'],
        created = data['created'],
        userId=user,
        categoryId=category
        )
    serializer = TopicSerializer(topics, many=False)
    return Response(serializer.data)
       
@api_view(['PUT'])
def updateTopic(request, pk):
    data = request.data

    topics = Topic.objects.get(topicId=pk)
    serializer = TopicSerializer(topics, data=request.POST)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTopic(request, pk):
    topics = Topic.objects.get(topicId=pk)
    topics.delete()
    return Response('Topic deleted!')

# COMMENTS
@api_view(['GET'])
def viewComments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addComment(request):
    data = request.data
    topicId = data['topicId']
    userId = data['userId']
    topics = Topic.objects.get(pk=topicId)
    user = User.objects.get(pk=userId)
    comment = Comment.objects.create(
        commentId=data['commentId'],
        content=data['content'],
        showReply=data['showReply'],
        userId=user,
        topicId=topics
    )
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
    
@api_view(['PUT'])
def updateComment(request, pk):
    data = request.data
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, data=request.POST)
    if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return Response('Comment deleted!')