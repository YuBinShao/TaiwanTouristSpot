from django.db import models


class Content(models.Model):
    
    text = models.TextField()
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 20)

    def __str__(self):
        return 'content'

# Create your models here.
class Scene(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    name = models.TextField()
    hot = models.CharField(max_length = 20)
    img = models.URLField()
    slug = models.TextField(default = '')

    def __str__(self):
        return self.name

class Characteristic(models.Model):
    scene = models.ForeignKey(Scene,on_delete=models.CASCADE)
    character = models.CharField(max_length = 15)
    def __str__(self):
        return 'Characteristic'