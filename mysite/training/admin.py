from django.contrib import admin
from .models import User, Statistic, Training_session, Training_mode, Difficulty_level, Exercise
# Register your models here.
admin.site.register(User)
admin.site.register(Statistic)
admin.site.register(Training_session)
admin.site.register(Training_mode)
admin.site.register(Difficulty_level)
admin.site.register(Exercise)