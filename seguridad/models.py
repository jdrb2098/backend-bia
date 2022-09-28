from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
class Paises(models.Model):
    nombre = models.CharField(max_length=50, db_column='T003nombre')
    pais = models.CharField(max_length=50, db_column="T003CodPais")
    class Meta:
        db_table = "T003Paises"
