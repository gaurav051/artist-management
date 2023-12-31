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


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		data = request.data
		serializer = UserRegisterSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			now = datetime.datetime.now()
			password = make_password(data['password'])
			cursor = connection.cursor()
			query = 'insert into user (email, password, dob,is_superuser,is_staff,is_active, first_name, last_name, address, phone, gender,created_at, updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
			cursor.execute(query,[data["email"], str(password),data["dob"], "0","0","1",data["first_name"],data["last_name"],data["address"],data["phone"],data["gender"],str(now),str(now)])
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
		cursor = connection.cursor()
		cursor.execute("select id, email, role_type, first_name, last_name, phone, dob,gender,address, is_superuser from user where id=%s",[str(request.user.id),])
		data = dictfetchall(cursor)
		
		# serializer = UserSerializer(request.user)
		return Response({'user': data[0]}, status=status.HTTP_200_OK)


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
		if request.user.role_type == 'super admin' or request.user.is_superuser:
			cursor = connection.cursor()
			cursor.execute("select id, email, role_type, first_name, last_name, phone, dob,gender,address from user where id!=%s",[str(request.user.id),])
			data = dictfetchall(cursor)
		elif request.user.role_type == 'artist manager':
			cursor = connection.cursor()
			cursor.exceute("select id, email, role_type, first_name, last_name, phone, dob,gender,address from user where role_type in ('artist manager','artist') and id!=%s",[str(request.user.id),])
			data = dictfetchall(cursor)
		else:
			data=[]
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
			user_query = 'update user set first_name=%s,last_name=%s,dob=%s,gender=%s,phone=%s,address=%s where id =%s;'

			cursor.execute(user_query,[data['first_name'],data["last_name"],data["dob"],data["gender"],data["phone"],data["address"],str(pk)] )
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateUser(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		data = request.data
		serilizer= UserCreateSerializer(data = data)
		if serilizer.is_valid():
			now = datetime.datetime.now()
			password = make_password(data['password'])
			cursor = connection.cursor()
			query = 'insert into user (email, password, dob,is_superuser,is_staff,is_active, first_name, last_name, address, phone, gender, role_type,created_at, updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
			cursor.execute(query,[data["email"], str(password),data["dob"], "0","0","1",data["first_name"],data["last_name"],data["address"],data["phone"],data["gender"],data["role_type"],str(now),str(now)])
			return Response({"message":"Data updated successfully"},status=status.HTTP_200_OK)
		else:
			return Response({"data":serilizer.errors},status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self,request):
		user_id = request.data["id"]
		cursor = connection.cursor()
		cursor.execute("delete from music where id in (select m.id from music m inner join artist a on a.id=m.artist_id inner join user u on u.id=a.user_id where u.id =" + str(user_id) +")")
		cursor.execute("delete from artist where id in (select a.id from artist a inner join user u on u.id=a.user_id where u.id = " + str(user_id)+")")
		query = "Delete from user where id="+str(user_id)
		cursor.execute(query)
		return Response({"message":"Data deleted successfully"},status=status.HTTP_200_OK)


