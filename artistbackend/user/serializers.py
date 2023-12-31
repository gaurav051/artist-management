from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('first_name','last_name','email','password','gender','dob','phone','address')

class UserCreateSerializer(serializers.ModelSerializer):
	role_type = serializers.CharField(required=True)
	gender = serializers.CharField(required=True)
	class Meta:
		model = UserModel
		fields = ('first_name','last_name','email','password','gender','dob','phone','address','password','role_type')
	# def create(self, clean_data):
	# 	user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'], role_type= clean_data['password'], gender=clean_data['password'],dob = )
	# 	user_obj.save()
	# 	return user_obj


class UserDataSerilizer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('id','first_name','last_name','email','gender','dob','phone','address','role_type')

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'role_type')