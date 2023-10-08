from django.db import models
from user.models import Users

# Create your models here.
class Artist(models.Model):
    class Meta:
        db_table = "artist"
    
    name = models.CharField(max_length=255)
    first_release_year = models.SmallIntegerField()
    no_of_albums_releases = models.PositiveIntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Music(models.Model):
    GENRE = [('rnb','rnb'),('country','country'),('classic','classic'),('rock','rock'),('jazz','jazz')]
    class Meta:
        db_table ="music"
    artist = models.ForeignKey('Artist', related_name='', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    genre = models.CharField(choices = GENRE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
