from django.apps import AppConfig

#this file is called "apps" but is more of a config file for the app


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
