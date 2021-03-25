from django.db import models

# Create your models here.


class Chef(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    ingredients = models.TextField(null=False)
    preparation_mode = models.TextField(null=False)
    date = models.DateField(auto_now_add=True)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, null= False)

    def __str__(self):
        return self.title
