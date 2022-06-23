from django.db import models

# Create your models here.

class Images(models.Model):
    name = models.CharField(max_length=100)
    imagen = models.BinaryField()
    slug = models.SlugField(unique=True)
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}, {self.imagen}, {self.slug}, {self.descripcion}'


