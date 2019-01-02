from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from training.forms import SignUpForm, NewPasswordForm, TrainingDescriptionForm
from .models import PresetTrainingSession, TrainingSession, GameSession, CaptureSession, ColorStimuli
from django.forms import model_to_dict
import json


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            form = PasswordChangeForm(request.user)
            messages.success(request, 'Tu contraseña ha sido actualizada')           
            return  render(request, 'training/password.html',{'form': form})
        else:
            messages.error(request, 'Las contraseña no coincide')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'training/password.html', {'form': form})


def login(request):
    return render(request, 'registration/login.html')

@login_required(login_url='login/')
def index(request):
    return render(request, 'training/homepage.html')

@login_required(login_url='login/')
def training(request):
    if request.method == 'POST':
        form = TrainingDescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sesionEntrenamiento')
    else:
        form = TrainingDescriptionForm()
        return render(request, 'training/entrenamiento.html', {'form': form})

@login_required(login_url='login/')
def games(request):
    games_list = PresetTrainingSession.objects.order_by('id')
    return render(request, 'training/games.html', {'games_list':games_list})

@login_required(login_url='login/')
def instrucciones(request):
    games_list = PresetTrainingSession.objects.order_by('id')
    return render(request, 'training/instrucciones.html', {'games_list':games_list} )

@login_required(login_url='login/')
def capture_mode(request):
    return render(request, 'training/modo_captura.html')

@login_required(login_url='login/')
def configuration(request):
    return render(request, 'training/config.html')

@login_required(login_url='login/')
def faq(request):
    return render(request, 'training/faq.html')

@login_required(login_url='login/')
def contact(request):
    return render(request, 'training/contact.html')

@login_required(login_url='login/')
def colorConfiguration(request):
    return render(request, 'training/colors.html')

@login_required(login_url='login/')
def saveColor(request):
    color = request.POST.get('group_radio')
    print(color)
    if request.method == 'POST':
        if color != None:
            config = ColorStimuli(
                user=request.user,
                color=color,
            )
            config.save()
            messages.success(request, 'Se ha actualizado el color correctamente')
            return render(request, 'training/colors.html')
        else:
            messages.warning(request, '¡Debes seleccionar un color!')
            return render(request, 'training/colors.html')


@login_required(login_url='login/')
def user(request):
    username = request.user
    user_training = TrainingSession.objects.filter(user=request.user)
    user_games = GameSession.objects.filter(user=request.user)
    user_captures = CaptureSession.objects.filter(user=request.user)
    return render(request, 'training/user.html')

@login_required(login_url='login/')
def createSession(request):
    form = TrainingDescriptionForm(request.POST)
    if form.is_valid():
        description = form.save(commit=True)
        print(description)
        session = TrainingSession(
            user=request.user,
            description=description,
        )
        session.save()
    
        return redirect('sesionEntrenamiento/{}'.format(session.id))

    #TODO: SHOW ERROR

@login_required(login_url='login/')
def sessionTraining(request, session_id):
    session_pk = session_id
    session = TrainingSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    description_of_session = model_to_dict(session.description)
    return render(request, 'training/sesionEntrenamiento.html', {
        'data_of_session': json.dumps(data_of_session),
        'description_of_session': json.dumps(description_of_session)
    } )

@login_required(login_url='login/')
def trainingResults(request):
    session_pk = request.POST.get('session_id')
    session = TrainingSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    return render(request, 'training/resultados.html', {
        'data_of_session': json.dumps(data_of_session),
    } )
       

@login_required(login_url='login/')
def createGame(request):
    games_list = PresetTrainingSession.objects.all()
    game = request.POST.get('group_radio')
    if request.method == 'POST':
        if game != None:
            session = GameSession
            game_selected = PresetTrainingSession.objects.get(name=game)
            session = GameSession(
            user=request.user,
            description=game_selected,
            )
            session.save()
            return redirect('sesionJuego/{}'.format(session.id))
        else:
            messages.warning(request, '¡Debes seleccionar un juego!')
            return render(request, 'training/games.html', {'games_list':games_list})


@login_required(login_url='login/')
def sessionGame(request, session_id):
    session_pk = session_id
    session = GameSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    description_of_session = model_to_dict(session.description)
    return render(request, 'training/sesionJuego.html', {
        'data_of_session': json.dumps(data_of_session),
        'description_of_session': json.dumps(description_of_session)    
    } )

@login_required(login_url='login/')
def gameResults(request):
    session_pk = request.POST.get('session_id')
    session = GameSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    return render(request, 'training/resultados.html', {
        'data_of_session': json.dumps(data_of_session),
    } )

@login_required(login_url='login/')
def createCapture(request):
        time_activation = request.POST.get('time_activation')
        if time_activation != 0:
            session = CaptureSession(
                user=request.user,
                time_activation=time_activation
            )
            session.save()
            return redirect('sesionCaptura/{}'.format(session.id))

    #TODO: SHOW ERROR

@login_required(login_url='login/')
def sessionCapture(request, session_id):
    session_pk = session_id
    session = CaptureSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    return render(request, 'training/sesionCaptura.html', {
        'data_of_session': json.dumps(data_of_session),
    } )


@login_required(login_url='login/')
def captureResults(request):
    session_pk = request.POST.get('session_id')
    session = CaptureSession.objects.get(pk=session_pk)
    data_of_session = model_to_dict(session)
    return render(request, 'training/resultados.html', {
        'data_of_session': json.dumps(data_of_session),
    } )

@login_required(login_url='login/')
def saveTrainingResults(request):
    results_training = request.POST.get('generate_results')
    results_to_store = json.loads(json.dumps(results_training))
    session_pk = request.POST.get('session_id')
    session = TrainingSession.objects.get(pk=session_pk)
    if request.method == 'POST':
        if session != None:
            session.results = results_to_store
            session.save()
            data_of_session = model_to_dict(session)
            return render(request, 'training/entrenamientoGuardado.html', {
                'data_of_session': json.dumps(data_of_session),
            } )
        else:
            return HttpResponse(status=400)

@login_required(login_url='login/')
def saveGameResults(request):
    results_game = request.POST.get('generate_results')
    results_to_store = json.loads(json.dumps(results_game))
    print(results_to_store)
    session_pk = request.POST.get('session_id')
    game = GameSession.objects.get(pk=session_pk)
    if request.method == 'POST':
        if game != None:
            game.results = results_to_store
            game.save()
            data_of_session = model_to_dict(game)
            return render(request, 'training/gamesGuardado.html', {
                'data_of_session': json.dumps(data_of_session),
            } )
        else:
            return HttpResponse(status=400)


@login_required(login_url='login/')
def saveCaptureResults(request):
    results_capture = request.POST.get('generate_results')
    results_to_store = json.loads(json.dumps(results_capture))
    session_pk = request.POST.get('session_id')
    session = CaptureSession.objects.get(pk=session_pk)
    if request.method == 'POST':
        if session != None:
            session.results = results_to_store
            session.save()
            data_of_session = model_to_dict(session)
            return render(request, 'training/modo_capturaGuardado.html', {
                'data_of_session': json.dumps(data_of_session),
            } )
        else:
            return HttpResponse(status=400)

@login_required(login_url='login/')
def trainingList(request):
    session_list = TrainingSession.objects.filter(user=request.user)
    return render(request,'training/trainingsession_list.html', {'session_list': session_list})

@login_required(login_url='login/')
def gamingList(request):
    session_list = GameSession.objects.filter(user=request.user)
    return render(request,'training/gaming_list.html', {'session_list': session_list})

@login_required(login_url='login/')
def captureList(request):
    session_list = CaptureSession.objects.filter(user=request.user)
    return render(request,'training/capturesession_list.html', {'session_list': session_list})

@login_required(login_url='login/')
def consultTraining(request):
    id_pk = request.POST.get('group_radio')
    if request.method == 'POST':
        if id_pk != None:
            session = TrainingSession.objects.get(id=id_pk)
            data_of_session = model_to_dict(session)
            return render(request, 'training/consult.html', {
                'data_of_session': json.dumps(data_of_session),
            })
        else:
            session_list = TrainingSession.objects.filter(user=request.user)
            messages.warning(request, '¡Debes seleccionar una opción!')
            return render(request, 'training/trainingsession_list.html', {'session_list': session_list})


@login_required(login_url='login/')
def consultGame(request):
   id_pk = request.POST.get('group_radio')
   if request.method == 'POST':
        if id_pk != None:
            session = GameSession.objects.get(id=id_pk)
            data_of_session = model_to_dict(session)
            return render(request, 'training/consult.html', {
                'data_of_session': json.dumps(data_of_session),
            })
        else:
            session_list = GameSession.objects.filter(user=request.user)
            messages.warning(request, '¡Debes seleccionar una opción!')
            return render(request, 'training/gaming_list.html')

@login_required(login_url='login/')
def consultSession(request):
    id_pk = request.POST.get('group_radio')
    if request.method == 'POST':
        if id_pk != None:
            session = CaptureSession.objects.get(id=id_pk)
            data_of_session = model_to_dict(session)
            return render(request, 'training/consult.html', {
                'data_of_session': json.dumps(data_of_session),
            })
        else:
            session_list = CaptureSession.objects.filter(user=request.user)
            messages.warning(request, '¡Debes seleccionar una opción!')
            return render(request, 'training/capturesession_list.html')
    
    
