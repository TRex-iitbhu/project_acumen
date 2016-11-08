from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

matrix = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
]

def LDRView(request):
    template_name = 'index.html'

    context = {
        'swarmBots':SwarmBot.objects.all()
    }

    return render(request,template_name,context)

def sensorView(request):
    template_name = 'sensor.html'

    context = {
        'swarmBots':SwarmBot.objects.all()
    }

    return render(request,template_name,context)
@csrf_exempt
def matrixUpdate(request, swarmBotId, reading):
    pass
    
@csrf_exempt
def LdrPostView(request,swarmBotId,ldr_reading):
    if request.method == "POST":
        print(swarmBotId,ldr_reading)
        Bot = SwarmBot.objects.get(swarmBotId=swarmBotId)
        ldr = LDR.objects.get(swarmBot = Bot)
        ldr.reading = ldr_reading
        ldr.save()

        return HttpResponse('recorded')


@csrf_exempt
def DsPostView(request,swarmBotId,ds_reading):
    if request.method == "POST":
        print(swarmBotId, ldr_reading)
        Bot = SwarmBot.objects.get(swarmBotId=swarmBotId)
        ds = DS.objects.get(swarmBot = Bot)
        ds.ds_reading = ds_reading
        ds.save()

        return HttpResponse('recorded')
