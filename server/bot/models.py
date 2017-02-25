from django.db import models

class SwarmBot(models.Model):
    swarmBotId = models.AutoField(primary_key=True)
    swarmBotName = models.CharField(max_length=50)
    patchStatus = models.BooleanField(default=False)
    row = models.IntegerField(blank=True,null=True)
    col = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return '%s - %s' %(self.swarmBotId, self.swarmBotName)

'''
Step Response technique
http://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/
'''

class IR(models.Model):
    swarmBot = models.OneToOneField(SwarmBot)
    irId = models.IntegerField()
    reading = models.BooleanField(default=False)

    def __str__(self):
        return '%s-%s' %(self.irId,self.reading)

class DS(models.Model):
    swarmBot = models.OneToOneField(SwarmBot)
    dsId = models.IntegerField()
    reading = models.FloatField()

    def __str__(self):
        return '%s-%s' %(self.dsId,self.reading)
