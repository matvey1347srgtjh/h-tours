from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account1'
    verbose_name = 'Аккакунт'


    def ready(self) -> None:
        import  account1.signals