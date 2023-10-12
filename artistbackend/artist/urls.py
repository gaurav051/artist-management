from django.urls import path
from . import views

urlpatterns = [
    #  url(r'^api-token-auth/', obtain_jwt_token),
	path('get/artist/list/', views.GetArtistList.as_view()),
    path('create/artist/', views.CreateArtist.as_view()),
    path('update/artist/<int:pk>/', views.UpdateArtist.as_view()),


    
    path('get/songs-list/<int:pk>', views.GetSongList.as_view()),
    path('create/songs-list/', views.CreateSong.as_view()),
    path('update/song/<int:pk>/', views.UpdateSong.as_view()),

    
    path('get/songs/', views.GetSelfSongList.as_view()),
    path('get/sample-artist/', views.GetSampleArtistFile.as_view()),
    path('get/sample-song/', views.GetSampleSongFile.as_view()),
    path('song/bulk-create/', views.SongBulkUpdate.as_view()),

    path('delete/artist/', views.DeleteArtist.as_view()),
    path('delete/song/', views.DeleteSong.as_view()),

    

    

]