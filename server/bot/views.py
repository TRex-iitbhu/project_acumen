from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
global matrix

def refresh(request):
    for ir in IR.objects.all():
        ir.reading = False
        ir.save()
    for bot in SwarmBot.objects.all():
        bot.patchStatus = False
        if bot.swarmBotId == 1:
            bot.row = 0
            bot.col = 0
        else:
            bot.row = 2
            bot.col = 4
        bot.save()

    return HttpResponse("<h3> Data refreshed </h3>")



@csrf_exempt
def matrixUpdate(request,swarmBotId,block):
    sb = SwarmBot.objects.get(swarmBotId=swarmBotId)
    rowList = [0,1,2,2,1,0]
    block = int(block)
    row = rowList[block % 6]
    col = int(block / 3)
    if swarmBotId == '1':
        sb.row = row
        sb.col = col
    else:
        print (swarmBotId)
        sb.row = 2 - row
        sb.col = 4 - col
    sb.save()
    print (swarmBotId, row, col)
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
IR & DS readings saving to the database
'''
@csrf_exempt
def sensorReadView(request, swarmBotId):
    if request.method == 'POST':
        post = request.POST
        status = int(post.get('status'))
        sensor = post.get('sensor')
        if sensor == 'ir':
            Bot = SwarmBot.objects.get(swarmBotId=swarmBotId)
            ir = IR.objects.get(swarmBot = Bot)
            r = post.get('reading')
            ir.reading = True if int(r)>0 else False
            ir.save()
        if sensor == 'ds':
            Bot = SwarmBot.objects.get(swarmBotId=swarmBotId)
            ds = DS.objects.get(swarmBot = Bot)
            reading = float(post.get('reading'))
            ds.reading = reading
            ds.save()

    return HttpResponse("done")
'''
Patch status update
'''
def patchStatusUpdate(request,swarmBotId,boolint):
    sb = SwarmBot.objects.get(swarmBotId=swarmBotId)
    if int(boolint):
        sb.patchStatus = True
    else:
        sb.patchStatus = False
    sb.save()
    return HttpResponse('done')

'''
ajax value check functions
'''

def blockCheck(request, id):
    sb = SwarmBot.objects.get(swarmBotId = id)
    return HttpResponse( str((sb.row,sb.col)) )


def dsvalue(request, id):
    ds = DS.objects.get(dsId = id)
    return  HttpResponse(ds.reading)

def irvalue(request, id):
    ir = IR.objects.get(irId = id)
    return  HttpResponse(ir.reading)

def patchStatus(request, id):
    bot = SwarmBot.objects.get(swarmBotId = id)
    return  HttpResponse(bot.patchStatus)
