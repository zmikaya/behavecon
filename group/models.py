from django.db import models

# Create your models here.
class Session(models.Model):
    name = models.CharField(max_length=128, unique=True)
    players = models.IntegerField()
    active_players = models.CharField(max_length=10000)
    stype = models.IntegerField(max_length=128)
    date = models.CharField(max_length=128)
    live = models.IntegerField()
    groups = models.CharField(max_length=10000, default='{"0": 0}')

    def __unicode__(self): 
        return self.name
        
class Player(models.Model):
    username = models.CharField(max_length=128, unique=True)
    session = models.CharField(max_length=128)
    group = models.IntegerField()
    info_set = models.IntegerField()
    state = models.CharField(max_length=128)
    time = models.CharField(max_length=1000)
    chat_room = models.CharField(max_length=128)
    answers = models.CharField(max_length=10000)
    
    def __unicode__(self):
        return self.username