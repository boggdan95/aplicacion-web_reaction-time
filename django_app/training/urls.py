from django.urls import path, re_path
from django.contrib.auth import views as auth_views


from . import views

app_name = 'trainig'
urlpatterns = [
    re_path('login', auth_views.LoginView.as_view(), name='login'),
    re_path('register', views.signup, name='signup'),
    re_path('password', views.change_password, name='password'),
    re_path('homepage', views.index, name='index'),
    re_path('entrenamiento', views.training, name='training'),
    re_path('games', views.games, name='games'),
    re_path('instrucciones', views.instrucciones, name='instructions'),
    re_path('config', views.configuration, name='configuration'),
    re_path('faq', views.faq, name='faq'),
    re_path('contact', views.contact, name='contact'),
    re_path('modo_captura', views.capture_mode, name='captura'),
    re_path('createSession',views.createSession, name='createSession'),
    re_path('createGame',views.createGame, name='createGame'),
    re_path('createCapture',views.createCapture, name='createCapture'),
    re_path('saveTrainingResults',views.saveTrainingResults, name='saveTrainingResults'),
    re_path('saveGameResults',views.saveGameResults, name='saveGameResults'),
    re_path('saveCaptureResults',views.saveCaptureResults, name='saveCaptureResults'),
    path('sesionEntrenamiento/<int:session_id>/', views.sessionTraining, name='sessionTraining'),
    path('sesionJuego/<int:session_id>/', views.sessionGame, name='sessionGame'),
    path('sesionCaptura/<int:session_id>/', views.sessionCapture, name='sessionCapture'),
    re_path('colors', views.colorConfiguration , name='colorConfiguration'),
    re_path('saveColor',views.saveColor, name='saveColor'),
    re_path('trainingResults', views.trainingResults , name='training_results'),
    re_path('gameResults', views.gameResults , name='game_results'),
    re_path('captureResults', views.captureResults , name='game_results'),
    re_path('user', views.user , name='user'),
    re_path('trainingsession_list', views.trainingList, name='trainingList'),
    re_path('gaming_list', views.gamingList, name='gameList'),
    re_path('capturesession_list', views.captureList, name='captureList'),
    re_path('consultTraining', views.consultTraining, name='consultTraining'),
    re_path('consultGame', views.consultGame, name='consultGame'),
    re_path('consultSession', views.consultSession, name='consultSession'),
]