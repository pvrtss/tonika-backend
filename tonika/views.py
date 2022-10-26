from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tonika.serializers import SongSerializer, AuthorSerializer, FolderSerializer, UserSerializer
from tonika.models import Song, Author, Folder, User


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('name')
    serializer_class = SongSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class FolderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Folder.objects.all().order_by('name')
    serializer_class = FolderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('login')
    serializer_class = UserSerializer


@api_view(['POST'])
def upload_image(request):
    data = request.data

    obj_id = data['pk']
    obj = Song.objects.get(id=obj_id)

    obj.image = request.FILES.get('image')
    obj.save()

    return Response('Image was uploaded')
