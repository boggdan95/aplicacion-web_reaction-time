from django.contrib import admin

# Register your models here.

from .models import TrainingDescription, TrainingSession, PresetTrainingSession, GameSession, CaptureSession

admin.site.register(TrainingDescription)
admin.site.register(TrainingSession)
admin.site.register(PresetTrainingSession)
admin.site.register(GameSession)
admin.site.register(CaptureSession)
