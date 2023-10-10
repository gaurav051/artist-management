from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
import datetime
UserModel = get_user_model()
from django.db import connection

from collections import namedtuple


def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    Assume the column names are unique.
    """
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class GetArtistList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		if request.user.role_type == 'super admin' or request.user.role_type == 'artist manager':

			query = "select * from artist;"
			artist = Artist.objects.raw(query)
			# cursor=connection.cursor()
			# cursor.execute("select * from artist")
			# row = cursor.fetchall()

			# print(row)
			# artist = Artist.objects.all()
			serilizer= GetArtistSerializer(artist, many=True)
			data = serilizer.data
			print(data)
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)
# Create your views here.

class UpdateArtist(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request, pk):
		# if request.user.role_type == 'super admin':
		artist = Artist.objects.get(id=pk)
		data = request.data
		serilizer= ArtistUpdateSerializer(data = request.data)
		if serilizer.is_valid():
			cursor = connection.cursor()
			artist_query = 'select * from artist where id="'+str(pk)+'";'
			print(artist_query)
			cursor.execute(artist_query)
			user = namedtuplefetchall(cursor)
			name = data['first_name'] + ' ' +  data['last_name']
			user_id = user[0].user_id
			print(user_id)
			query = 'update artist set name="'+name+'",first_release_year="'+request.data["first_release_year"]+'",no_of_albums_releases="'+request.data["no_of_albums_releases"]+'" where id="'+str(pk)+'";'
			cursor.execute(query)

			user_query = 'update user set first_name="'+data['first_name']+'",last_name="'+data["last_name"]+'",dob="'+data["dob"]+'",gender="'+data["gender"] +'",phone="'+data["phone"]+'",address="'+data["address"]+'" where id ="'+str(user_id)+'";'
			print(user_query)
			cursor.execute(user_query)
			# name = data['first_name'] + ' ' +  data['last_name']
			
			# query = 'update artist set title="'+name+'",first_release_year="'+request.data["first_release_year"]+'",no_of_albums_releases="'+request.data["no_of_albums_releases"]+'" where id="'+str(pk)+'";'
			# cursor.execute(query)
			
			# Artist.objects.update_or_create(pk=pk, defaults={"name":name,"first_release_year":data["first_release_year"],"no_of_albums_releases":data["no_of_albums_releases"]})
			# user = artist.user.id

			# UserModel.objects.update_or_create(pk=artist.user.id,defaults={"dob":data["dob"],"first_name" : data["first_name"],"last_name" : data["last_name"],"address":data["address"],"phone":data["phone"], "gender":data["gender"]})
			# user.update(dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"])
			
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateArtist(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		data = request.data
		serilizer= ArtistCreateSerializer(data = request.data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			
			password = make_password(self.request.data['password'])
			cursor = connection.cursor()
			query = 'insert into user (email, password, dob,is_superuser,is_staff,is_active, first_name, last_name, address, phone, gender, role_type,created_at, updated_at) values ("'+data["email"]+'","'+str(password)+'","'+data["dob"]+'","0","0","1","'+data["first_name"]+'","'+data["last_name"]+'","'+data["address"]+'","'+data["phone"]+'","'+data["gender"]+'","artist","'+str(now)+'","'+str(now)+'");'
			cursor.execute(query)
			print(cursor.lastrowid)
			name = data['first_name'] + ' ' +  data['last_name']

			query = 'insert into artist (name, first_release_year, no_of_albums_releases, user_id, created_at, updated_at) values ("'+name+'","'+data["first_release_year"]+'","'+data["no_of_albums_releases"]+'","'+str(cursor.lastrowid)+'","'+str(now)+'","'+str(now)+'");'
			print(query)
			cursor.execute(query)
			# user = UserModel.objects.create(email=data["email"],dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"], role_type='artist')
			# user.set_password(data["password"])
			# user.save()
			# name = data['first_name'] + ' ' +  data['last_name']
			# Artist.objects.create(name=name,first_release_year=data["first_release_year"],no_of_albums_releases = data["no_of_albums_releases"], user=user)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)


class GetSongList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request, pk):
		artist = Artist.objects.get(id=pk)
		if request.user.role_type == 'super admin' or request.user.role_type == 'artist manager':

			query = 'select * from music where artist_id ='+str(pk)+';'
			music = Music.objects.raw(query)
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
			cursor = connection.cursor()
			query = 'update music set title="'+request.data["title"]+'",album_name="'+request.data["album_name"]+'",genre="'+request.data["genre"]+'" where id="'+str(pk)+'";'
			print(query)
			cursor.execute(query)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateSong(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request,pk):
		artist = Artist.objects.get(id=pk)
		
		data = request.data
		serilizer= MusicCreateSerializer(data = request.data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			cursor = connection.cursor()
			query = 'INSERT INTO music (title,genre,album_name, artist_id, created_at,updated_at) VALUES( "'+data["title"]+'","'+data["genre"]+'","'+data["album_name"]+'","'+str(pk)+'","'+str(now)+'","'+str(now)+'");'
			print(query)
			cursor.execute(query)
			# Music.objects.create(title=data["title"], genre = data["genre"],album_name=data["album_name"], artist=artist)
			# user = UserModel.objects.create(email=data["email"],dob=data["dob"],first_name = data["first_name"],last_name = data["last_name"],address=data["address"],phone=data["phone"], gender=data["gender"], role_type='artist')
			# user.set_password(data["password"])
			# user.save()
			# name = data['first_name'] + ' ' +  data['last_name']
			# Artist.objects.create(name=name,first_release_year=data["first_release_year"],no_of_albums_releases = data["no_of_albums_releases"], user=user)
			return Response({"message":"Music Added successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

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