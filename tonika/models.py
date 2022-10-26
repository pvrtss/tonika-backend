from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'authors'

    def __str__(self):
        return '%s (id:%d)' % (self.name, self.id)


class Song(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    chords = models.CharField(max_length=10000)
    cover = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'songs'


class User(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    favourites = models.ManyToManyField(Song)

    class Meta:
        managed = True
        db_table = 'users'


class Folder(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'folders'
