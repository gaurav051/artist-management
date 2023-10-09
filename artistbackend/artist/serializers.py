from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from artist.models import Artist, Music

class ArtistCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    first_release_year = serializers.CharField(required=True)
    no_of_albums_releases = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    dob = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)


class ArtistUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    first_release_year = serializers.CharField(required=True)
    no_of_albums_releases = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    dob = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)


class GetArtistSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    phone= serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ('id','name','gender','dob','first_name','last_name','address','phone','email','first_release_year','no_of_albums_releases')
    
    def get_first_name(self,obj):
        return obj.user.first_name
    
    def get_last_name(self,obj):
        return obj.user.last_name
    def get_email(self,obj):
        return obj.user.email
    
    def get_gender(self,obj):
        return obj.user.gender
    
    def get_dob(self,obj):
        return obj.user.dob
    
    def get_address(self,obj):
        return obj.user.address
    
    def get_phone(self,obj):
        return obj.user.phone


class GetMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ("id","title","genre","album_name")


class MusicCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    genre = serializers.CharField(required=True)
    album_name = serializers.CharField(required=True)
    # class Meta:
    #     model = Music
    #     fields = ("id","title","genre","album")