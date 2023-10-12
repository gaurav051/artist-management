from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    #  url(r'^api-token-auth/', obtain_jwt_token),
	path('register', views.UserRegister.as_view(), name='register'),
	path('get-token', obtain_jwt_token, name='login'),
	path('logout/', views.LogoutAllView.as_view(), name='logout'),
	path('user/me', views.UserView.as_view(), name='user'),
    path('get/user-list/', views.GetUserList.as_view(), name='user-list'),
	path('add/user/', views.CreateUser.as_view(), name='add-user-list'),
	path('update/user/<int:pk>/', views.UpdateUser.as_view(), name='add-user-list'),
    
	path('delete/user/', views.DeleteUser.as_view()),
	

	
]