from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from .models import UserAccount, ColorUser, PostFile
from .serializers import (UserCreateSerializer, ColorUserSerializer, PostSerializer, PostFileSerializer,
                          LoginSerializer)

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


class UserAccountListView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer



class ColorUserListView(generics.ListCreateAPIView):
    queryset = ColorUser.objects.all()
    serializer_class = ColorUserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostSerializer


class GetAllFiles(APIView):
    def get(self, request):
        files = PostFile.objects.all()
        serializer = PostFileSerializer(files, many=True)
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                user.is_active = True
                user.save()

                # Создание или обновление токена пользователя
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key, 'user_id': user.id, 'name': user.name}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

