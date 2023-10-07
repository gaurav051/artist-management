from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    #  url(r'^api-token-auth/', obtain_jwt_token),
	path('register', views.UserRegister.as_view(), name='register'),
	path('get-token', obtain_jwt_token, name='login'),
	# path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
]