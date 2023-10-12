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
from pathlib import Path
UserModel = get_user_model()
from django.db import connection
import os
from django.conf import settings
from collections import namedtuple
from django.http import HttpResponse, HttpResponseNotFound


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
		data = request.data
		serilizer= ArtistUpdateSerializer(data = request.data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			cursor = connection.cursor()
			artist_query = 'select * from artist where id="'+str(pk)+'";'
			print(artist_query)
			cursor.execute(artist_query)
			user = namedtuplefetchall(cursor)
			name = data['first_name'] + ' ' +  data['last_name']
			user_id = user[0].user_id
			print(user_id)
			cursor.execute('update artist set name=%s,first_release_year=%s,no_of_albums_releases=%s,updated_at=%s where id=%s',[name,data["first_release_year"],data["no_of_albums_releases"],str(now),str(pk)])
			cursor.execute('update user set first_name=%s,last_name=%s,dob=%s,gender=%s,phone=%s,address=%s,updated_at=%s where id =%s',[data['first_name'],data["last_name"],data["dob"],data["gender"],data["phone"],data["address"],str(now),str(user_id)])
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
			cursor.execute('insert into user (email, password, dob,is_superuser,is_staff,is_active, first_name, last_name, address, phone, gender, role_type,created_at, updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[data["email"],str(password),data["dob"],"0","0","1",data["first_name"],data["last_name"],data["address"],data["phone"],data["gender"],"artist",str(now),str(now)])
			print(cursor.lastrowid)
			name = data['first_name'] + ' ' +  data['last_name']
			cursor.execute('insert into artist (name, first_release_year, no_of_albums_releases, user_id, created_at, updated_at) values (%s,%s,%s,%s,%s,%s)',[name,data["first_release_year"],data["no_of_albums_releases"],str(cursor.lastrowid),str(now),str(now)])
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
		data = request.data
		now = datetime.datetime.now()
		serilizer= MusicCreateSerializer(data = request.data)
		if serilizer.is_valid():
			cursor = connection.cursor()
			cursor.execute('update music set title=%s,album_name=%s,genre=%s,updated_at=%s where id=%s;',[data["title"],data["album_name"],data["genre"],str(now),str(pk)])
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateSong(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		data = request.data
		serilizer= MusicCreateSerializer(data = request.data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			
			cursor = connection.cursor()
			artist = "select * from artist where user_id="+str(request.user.id)+" limit 1;"
			cursor.execute(artist)
			# data = cursor.fetchone()
			artist_data = namedtuplefetchall(cursor)
			artist_id = artist_data[0].id
			print(artist_id)

			query = 'INSERT INTO music (title,genre,album_name, artist_id, created_at,updated_at) VALUES( "'+data["title"]+'","'+data["genre"]+'","'+data["album_name"]+'","'+str(artist_id)+'","'+str(now)+'","'+str(now)+'");'
			print(query)
			cursor.execute(query)
			return Response({"message":"Music Added successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class GetSelfSongList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		if request.user.role_type == 'artist':
			print(request.user.id)
			
			
			# query = 'select * from music where artist_id ='+str(pk)+';'
			music = Music.objects.raw('select m.id as id, title, album_name, genre from music m join artist a on a.id = m.artist_id join user u ON a.user_id = u.id where u.id=%s',[str(request.user.id)])
			serilizer= GetMusicSerializer(music, many=True)
			data = serilizer.data
			# artist = Artist.objects.filter(user=request.user).last()
			# music = Music.objects.filter(artist=artist)
			# serilizer= GetMusicSerializer(music, many=True)
			# data = serilizer.data
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)
	

class GetSampleArtistFile(APIView):
	permissions_classes =  (permissions.IsAuthenticated,)
	def get(self,request):
		BASE_DIR = Path(__file__).resolve().parent.parent
		print(BASE_DIR)
		file_location = BASE_DIR/'static/sampleartist.csv'
		print(file_location)
		try:    
			with open(file_location, 'r') as f:
				file_data = f.read()
				# sending response 
				response = HttpResponse(file_data, content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="sample.csv"'

		except IOError:
			# handle file not exist case here
			response = HttpResponseNotFound('<h1>File not exist</h1>')

		return response


class GetSampleSongFile(APIView):
	permissions_classes =  (permissions.IsAuthenticated,)
	def get(self,request):
		BASE_DIR = Path(__file__).resolve().parent.parent
		print(BASE_DIR)
		file_location = BASE_DIR/'static/songsample.csv'
		print(file_location)
		try:    
			with open(file_location, 'r') as f:
				file_data = f.read()
				# sending response 
				response = HttpResponse(file_data, content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="sample.csv"'

		except IOError:
			# handle file not exist case here
			response = HttpResponseNotFound('<h1>File not exist</h1>')

		return response

class SongBulkUpdate(APIView):
	permissions_classes =  (permissions.IsAuthenticated,)
	def post(self,request, pk):
		try:
			now = datetime.datetime.now()
			data = request.data
			cursor = connection.cursor()
			for i in data:
				cursor.execute("Insert into music (title,genre,album_name, artist_id, created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s)",[i["title"],i["album_name"],i["genre"],str(pk),str(now), str(now)])
			return Response({"meaasge":"data updated successfully"})
		except Exception as e:
			return Response({"data":str(e)}, status=status.HTTP_400_BAD_REQUEST)

