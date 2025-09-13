from django.apps import AppConfig
from .connections import *


class FilterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filter'
