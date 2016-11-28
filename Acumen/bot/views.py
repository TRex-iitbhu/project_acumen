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

@csrf_exempt
def sensorReadView(request):
    if request.method == 'POST':
        # print (request.POST)
#<QueryDict: {'status': ['0'], 'sensor': ['ds'], 'reading': ['68.13']}>
        post = request.POST
        status = int(post.get('status'))
        sensor = post.get('sensor')
        reading = float(post.get('reading'))
        print (reading)
        if sensor == 'ldr':
            Bot = SwarmBot.objects.get(swarmBotId=1)
            ldr = LDR.objects.get(swarmBot = Bot)
            ldr.reading = reading
            ldr.save()
        if sensor == 'ds':
            Bot = SwarmBot.objects.get(swarmBotId=1)
            ds = DS.objects.get(swarmBot = Bot)
            ds.reading = reading
            ds.save()
    return HttpResponse("done")

def dsvalue(request, id):
    print (request,id)
    ds = DS.objects.get(dsId = id)
    print (ds, ds.reading)
    value = float(ds.reading)
    return  HttpResponse(value)

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
