from django.contrib.auth import get_user_model, login, logout
from user.models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserDataSerilizer, UserCreateSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.hashers import make_password
from django.db import connection
import datetime


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = request.data
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			user.set_password(clean_data["password"])
			user.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)
	


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = [JSONWebTokenAuthentication]
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class LogoutAllView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)

class GetUserList(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		if request.user.role_type == 'super admin':

			query = '''select * from user where role_type in ('super admin','artist manager','artist') and id!="'''+str(request.user.id)+'''";'''
			users = User.objects.raw(query)
			# users = User.objects.filter(role_type__in=['super admin','artist manager','artist']).exclude(id=request.user.id)
			serilizer= UserDataSerilizer(users, many=True)
			data = serilizer.data
		elif request.user.role_type == 'artist manager':
			users = '''select * from user where role_type in ('artist manager','artist') and id!="'''+str(request.user.id)+'''";'''
			users = User.objects.raw(query)
			# users = User.objects.filter(role_type__in=['artist manager','artist']).exclude(id=request.user.id)
			serilizer= UserDataSerilizer(users, many=True)
			data = serilizer.data
		else:
			data=[]
		return Response({"data":data},status=status.HTTP_200_OK)

class GetUserByID(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request, pk):
		if request.user.role_type == 'super admin':
			users = User.objects.filter(role_type__in=['super admin','artist manager','artist'], id=pk).exclude(id=request.user.id).last()
			serilizer= UserDataSerilizer(users)
			data = serilizer.data
		elif request.user.role_type == 'artist manager':
			users = User.objects.filter(role_type__in=['artist manager','artist'], id=pk).exclude(id=request.user.id).last()
			serilizer= UserDataSerilizer(users)
			data = serilizer.data
		else:
			data={}
		return Response({"data":data},status=status.HTTP_200_OK)

class UpdateUser(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request, pk):
		# if request.user.role_type == 'super admin':
		users = User.objects.get(id=pk)
		serilizer= UserDataSerilizer(users,data = request.data)
		if serilizer.is_valid():
			data = request.data
			cursor = connection.cursor()
			user_query = 'update user set first_name="'+data['first_name']+'",last_name="'+data["last_name"]+'",dob="'+data["dob"]+'",gender="'+data["gender"] +'",phone="'+data["phone"]+'",address="'+data["address"]+'" where id ="'+str(pk)+'";'
			print(user_query)
			cursor.execute(user_query)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateUser(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		# if request.user.role_type == 'super admin':
		# users = User.objects.get(id=pk)
		data = request.data
		serilizer= UserCreateSerializer(data = data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			
			password = make_password(data['password'])
			cursor = connection.cursor()
			query = 'insert into user (email, password, dob,is_superuser,is_staff,is_active, first_name, last_name, address, phone, gender, role_type,created_at, updated_at) values ("'+data["email"]+'","'+str(password)+'","'+data["dob"]+'","0","0","1","'+data["first_name"]+'","'+data["last_name"]+'","'+data["address"]+'","'+data["phone"]+'","'+data["gender"]+'","'+data["role_type"]+'","'+str(now)+'","'+str(now)+'");'
			cursor.execute(query)
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)


