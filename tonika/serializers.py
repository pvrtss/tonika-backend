from tonika.models import Song, Author, Folder, User
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["pk", "name", "description"]


class SongSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name', )

    class Meta:
        model = Song
        fields = ["pk", "name", "chords", "author", "cover", "status", "date_added", "date_accepted", "date_declined"]


class FolderSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True)
    owner_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source="owner")

    class Meta:
        model = Folder
        fields = ["pk", "name", "description", "songs", "owner_id"]


class UserSerializer(serializers.ModelSerializer):
    favourites = SongSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ["pk", "username", "is_staff", "is_superuser", "favourites"]
