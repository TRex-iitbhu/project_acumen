from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
global matrix
matrix = [
    [1,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,2],
]

@csrf_exempt
def matrixUpdate(request,swarmBotId,row,col):
    global matrix
    if swarmBotId == '1':
        matrix[row][col] = 1
    elif swarmBotId == '2':
        matrix[row][col] = 2
    return HttpResponse('done')

def index(request):
    template_name = 'index.html'
    return render(request, template_name, {})

def sensorView(request):
    template_name = 'sensor.html'

    context = {
        'swarmBots':SwarmBot.objects.all()
    }

    return render(request,template_name,context)

'''
LDR & DS readings saving to the database
'''
@csrf_exempt
def sensorReadView(request):
    if request.method == 'POST':
        post = request.POST
        status = int(post.get('status'))
        reading = float(post.get('reading'))
        sensor = post.get('sensor')
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


'''
ajax value check functions
'''

def matUpdateWeb(request, id):
    global matrix
    for i in range(3):
        for j in range(5):
            if matrix[i][j] == int(id):
                # print (str((i,j)))
                return HttpResponse(str((i,j)))

    return HttpResponse('not found')


def dsvalue(request, id):
    ds = DS.objects.get(dsId = id)
    return  HttpResponse(ds.reading)

def ldrvalue(request, id):
    ldr = LDR.objects.get(ldrId = id)
    return  HttpResponse(ldr.reading)

def patchStatus(request, id):
    bot = SwarmBot.objects.get(swarmBotId = id)
    return  HttpResponse(bot.patchStatus)
