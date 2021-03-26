from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import ChefUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class ChefUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects= ChefUserManager()

    def get_full_name(self):
        full_name = '%s %s' (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.email



class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    ingredients = models.TextField(null=False)
    preparation_mode = models.TextField(null=False)
    date = models.DateField(auto_now_add=True)
    chef = models.ForeignKey(ChefUser, on_delete=models.CASCADE, null= False)
