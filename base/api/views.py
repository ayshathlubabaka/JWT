from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import User

from .serializers import UserSerializer, UserProfileSerializer, UserListSerializer, UserRegisterSerializer, UserUpdateSerializer, UserCreateSerializer
from base.models import UserProfile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
def getCsrf(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)


@api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_view(request):
    user = request.user
    if user:
        serializer = UserSerializer(user)
        data = serializer.data
        return Response(data)
    else:
        return Response({"detail": "User profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET', 'PUT', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):

    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()

    if request.method == 'GET':
        if user:
            serializer = UserProfileSerializer(user)
            data = serializer.data
            try:
                profile_picture = user_profile.profile_picture
                data['profile_picture'] = request.build_absolute_uri('/')[:-1]+profile_picture.url
            except:
                profile_picture = ''
                data['profile_picture'] = ''
            return Response(data)
        else:
            return Response({"detail": "User profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method in ('POST'):

        if user_profile:
            serializer = UserProfileSerializer(user_profile, data=request.data)
        else:
            serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
           
            if user_profile:
                if 'profile_picture' in request.FILES:
                    user_profile.profile_picture = request.FILES['profile_picture']
                    user_profile.save()

            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def user_list(request):
    user_list = User.objects.filter(is_superuser=False)
    serializer = UserListSerializer(user_list, many=True)
    data = serializer.data
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_create(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_crud(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print('inside delete')
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

