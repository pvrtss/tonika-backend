from django.utils import timezone
from rest_framework import viewsets, status
import datetime
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from tonika.permissions import ManagerOrReadOnly, ManagerOnly, DefaultUser
from tonika.serializers import SongSerializer, AuthorSerializer, FolderSerializer, UserSerializer
from tonika.models import Song, Author, Folder, User

from django.contrib.auth import authenticate
from django.http import HttpResponse

from django.conf import settings
import redis
import uuid

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@api_view(["POST"])
def create_user(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    u = User.objects.create_user(username=username, password=password)
    if u is not None:
        return HttpResponse("{'status': 'ok'}")
    else:
        return HttpResponse("{'status': 'error', 'error': 'user creation failed'}")


@api_view(["GET"])
def logout(request):
    ssid = request.COOKIES.get("session_id")
    if ssid is not None:
        session_storage.delete(ssid)
        return Response(status=status.HTTP_200_OK, data="{\"status\": \"successfully logged out\"}")
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            key = str(uuid.uuid4())
            session_storage.set(key, username)
            u = User.objects.get(username=username)
            u.last_login = timezone.now()
            u.save()
            response = Response("{\"status\": \"ok\"}", content_type="json")
            response.set_cookie("session_id", key)
            return response
        else:
            return Response("{\"status\": \"error\", \"error\": \"login failed\"}")


class NewSongsList(APIView):
    def get(self, request):
        ssid = request.COOKIES.get("session_id")
        if ssid is not None and session_storage.get(ssid) is not None:
            response = SongSerializer(Song.objects.all().order_by('-date_added')[:10], many=True)
            return Response(response.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [ManagerOrReadOnly]

    def get_queryset(self):
        from_year = self.request.query_params['from'] if 'from' in self.request.query_params else 1
        to_year = self.request.query_params['to'] if 'to' in self.request.query_params else datetime.date.today().year
        name = self.request.query_params['name'] if 'name' in self.request.query_params else ''
        author = self.request.query_params['author'] if 'author' in self.request.query_params else ''
        return Song.objects.filter(date_added__year__gte=from_year,
                                   date_added__year__lte=to_year,
                                   name__icontains=name,
                                   author__name__icontains=author).order_by('name')

    serializer_class = SongSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [ManagerOrReadOnly]
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


@api_view(['POST'])
@permission_classes([DefaultUser])
def create_folder(request):
    user = User.objects.get(username=session_storage.get(request.COOKIES.get('session_id')).decode())
    f = Folder.objects.create()
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [ManagerOnly]
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


@api_view(['POST'])
def upload_image(request):
    data = request.data

    obj_id = data['pk']
    obj = Song.objects.get(id=obj_id)

    obj.image = request.FILES.get('image')
    obj.save()

    return Response('Image was uploaded')
