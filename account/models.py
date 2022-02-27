from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    company_id = models.CharField(max_length=200)
    organizations_name = models.CharField(max_length=200)
    organizations_address = models.CharField(max_length=200)
    requisites = models.CharField(max_length=200)

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)
