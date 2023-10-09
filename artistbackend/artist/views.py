from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model, authenticate
UserModel = get_user_model()


class GetArtistList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		if request.user.role_type == 'super admin' or request.user.role_type == 'artist manager':
			artist = Artist.objects.all()
			serilizer= GetArtistSerializer(artist, many=True)
			data = serilizer.data
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)
# Create your views here.
class GetArtistByID(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request, pk):
		if request.user.role_type == 'super admin' or request.user.role_type == 'artist manager':
			artist = Artist.objects.all()
			serilizer= GetArtistSerializer(artist)
			data = serilizer.data
		else:
			data={}
		return Response({"data":data},status=status.HTTP_200_OK)

class UpdateArtist(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request, pk):
		# if request.user.role_type == 'super admin':
		artist = Artist.objects.get(id=pk)
		data = request.data
		serilizer= ArtistUpdateSerializer(data = request.data)
		if serilizer.is_valid():
			name = data['first_name'] + ' ' +  data['last_name']
			
			Artist.objects.update_or_create(pk=pk, defaults={"name":name,"first_release_year":data["first_release_year"],"no_of_albums_releases":data["no_of_albums_releases"]})
			user = artist.user.id

			UserModel.objects.update_or_create(pk=artist.user.id,defaults={"dob":data["dob"],"first_name" : data["first_name"],"last_name" : data["last_name"],"address":data["address"],"phone":data["phone"], "gender":data["gender"]})
			# user.update(dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"])
			
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors})

class CreateArtist(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		data = request.data
		serilizer= ArtistCreateSerializer(data = request.data)
		if serilizer.is_valid():
			user = UserModel.objects.create(email=data["email"],dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"], role_type='artist')
			user.set_password(data["password"])
			user.save()
			name = data['first_name'] + ' ' +  data['last_name']
			Artist.objects.create(name=name,first_release_year=data["first_release_year"],no_of_albums_releases = data["no_of_albums_releases"], user=user)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors})


class GetSongList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request, pk):
		artist = Artist.objects.get(id=pk)
		if request.user.role_type == 'super admin' or request.user.role_type == 'artist manager':
			music = Music.objects.filter(artist=artist)
			serilizer= GetMusicSerializer(music, many=True)
			data = serilizer.data
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)
# Create your views here.


class UpdateSong(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request, pk):
		# if request.user.role_type == 'super admin':
		# artist = Music.objects.get(id=pk)
		data = request.data
		serilizer= MusicCreateSerializer(data = request.data)
		if serilizer.is_valid():
			
			
			Music.objects.update_or_create(pk=pk, defaults={"title":data["title"],"album_name":data["album_name"],"genre":data["genre"]})
			# user = artist.user.id

			# UserModel.objects.update_or_create(pk=artist.user.id,defaults={"dob":data["dob"],"first_name" : data["first_name"],"last_name" : data["last_name"],"address":data["address"],"phone":data["phone"], "gender":data["gender"]})
			# user.update(dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"])
			
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors})

class CreateSong(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request,pk):
		artist = Artist.objects.get(id=pk)
		
		data = request.data
		serilizer= MusicCreateSerializer(data = request.data)
		if serilizer.is_valid():
			Music.objects.create(title=data["title"], genre = data["genre"],album_name=data["album_name"], artist=artist)
			# user = UserModel.objects.create(email=data["email"],dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"], role_type='artist')
			# user.set_password(data["password"])
			# user.save()
			# name = data['first_name'] + ' ' +  data['last_name']
			# Artist.objects.create(name=name,first_release_year=data["first_release_year"],no_of_albums_releases = data["no_of_albums_releases"], user=user)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors})

class GetSelfSongList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		if request.users.role_type == 'artist':
			artist = Artist.objects.filter(user=request.user).last()
			music = Music.objects.filter(artist=artist)
			serilizer= GetMusicSerializer(music, many=True)
			data = serilizer.data
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)