from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator
from django.contrib.postgres.fields import JSONField


# Create your models here.

class TrainingDescription(models.Model):
    TIMES = ((30,'30'),(45,'45'),(60,'60'),(75,'75'),(90,'90'),(105,'105'),(120,'120'))
    MODULES = ((1,'1'),(2,'2'),(3,'3'),(4,'4'))
    REPS = ((10,'10'),(11,'11'),(12,'12'),(13,'13'),(14,'14'),(15,'15'),(16,'16'),(17,'17'),(18,'18'),(19,'19'),(20,'20'))
    SINGLE = 'SIMPLE'
    COMPLEX = 'COMPLEJO'
    TYPES = ((SINGLE,'Simple'),(COMPLEX,'Complejo'))
    typeReaction = models.CharField(max_length=10,choices=TYPES, default=SINGLE)
    time = models.IntegerField(choices=TIMES,default=30)
    reps = models.IntegerField(choices=REPS,default=10)
    modules = models.IntegerField(choices=MODULES,default=1)
    is_secuencial = models.BooleanField(default=True)

class TrainingSession(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='User', null=True)
    description = models.ForeignKey(TrainingDescription, on_delete=models.CASCADE)
    results = JSONField(null=True, blank=True) 



class PresetTrainingSession(models.Model):
    name = models.TextField(default='preset training')
    SINGLE = 'SIMPLE'
    COMPLEX = 'COMPLEJO'
    TYPES = ((SINGLE,'Simple'),(COMPLEX,'Complejo'))
    typeReaction = models.CharField(max_length=10,choices=TYPES, default=SINGLE)
    instructions = models.TextField()
    time = models.IntegerField(default=30)
    reps = models.IntegerField(default=10)
    modules = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ])
    is_secuencial = models.BooleanField(default=True)

class GameSession(models.Model):
    time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_user', null=True)
    description = models.ForeignKey(PresetTrainingSession, on_delete=models.CASCADE)
    results = JSONField(blank=True, null=True)
    

class CaptureSession(models.Model):
    time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='free_user', null=True)
    time_activation = models.IntegerField(default=1)
    results = JSONField(blank=True, null=True)

class PageGameSession(models.Model):
    time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='web_user', null=True)
    results = JSONField(blank=True, null=True)
    bestTime = models.IntegerField(blank=True, null=True)
    average = models.IntegerField(blank=True, null=True)

class ColorStimuli(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='color_user', null=True)
    color = models.CharField(blank=True, null=True, max_length=20)

class Question(models.Model):
    question_text = models.TextField(default='Pregunta')

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(default='Respuesta')

