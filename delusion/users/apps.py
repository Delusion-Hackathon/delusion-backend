from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delusion.users'

    def ready(self) -> None:
        from delusion.users.signals import create_mesh_user 
        from delusion import tasks
