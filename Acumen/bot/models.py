from django.db import models

class SwarmBot(models.Model):
    swarmBotId = models.AutoField(primary_key=True)
    swarmBotName = models.CharField(max_length=50)
    patchStatus = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' %(self.swarmBotId, self.swarmBotName)

'''
Step Response technique
http://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/
'''

class LDR(models.Model):
    swarmBot = models.OneToOneField(SwarmBot)
    reading = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return '%s - %s' %(self.swarmBot.swarmBotId, self.reading)

class IR(models.Model):
    swarmBot = models.ForeignKey(SwarmBot)
    irId = models.IntegerField()
    irReading = models.IntegerField()

    def __str__(self):
        return '%s-%s' %(self.irId,self.irReading)

class DS(models.Model):
    swarmBot = models.ForeignKey(SwarmBot)
    dsId = models.IntegerField()
    dsReading = models.IntegerField()

    def __str__(self):
        return '%s-%s' %(self.usId,self.usReading)
