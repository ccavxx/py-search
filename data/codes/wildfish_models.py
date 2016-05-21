from django.core.urlresolvers import reversefrom django.db import models

class {{ cookiecutter.model_name }}(models.Model):    name = models.CharField(max_length=255)
 def __str__(self): return self.name
 def get_absolute_url(self): return reverse('{{ cookiecutter.app_name }}:detail', args=[str(self.id)])