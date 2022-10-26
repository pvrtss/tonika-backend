from tonika.models import Song, Author, Folder, User
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["pk", "name", "description"]


class SongSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name',)

    class Meta:
        model = Song
        fields = ["pk", "name", "chords", "author", "cover", "date_added"]


class FolderSerializer(serializers.ModelSerializer):
    songs_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source="songs")
    owner_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source="owner")

    class Meta:
        model = Folder
        fields = ["pk", "name", "description", "songs_id", "owner_id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "login"]
