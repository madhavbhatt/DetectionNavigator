from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,Http404, HttpResponseRedirect
from attnav import *
from .models import *
from manageDB import *
from download import *
from update import *
import mysql.connector


def index(request):
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute('select * from DetectionChart_techniques')
    techrow = db_cursor.fetchall()

    if not techrow:
        dataPullMITRE()
        attnavupdateRepeats()
        print("pulling data for the first time")

        ttp = TTP.objects.all()
        tac = Tactic.objects.all()
        tech = Techniques.objects.all()

        all_dict = {'ttp': ttp, 'tac': tac, 'tech': tech}
        return render(request, 'base.html', all_dict)
    else:
        print("data already exists")
        ttp = TTP.objects.all()
        tac = Tactic.objects.all()
        tech = Techniques.objects.all()

        all_dict = {'ttp': ttp, 'tac': tac, 'tech': tech}
        return render(request, 'base.html', all_dict)


def detvalue(request):

    ttp = TTP.objects.all()
    tac = Tactic.objects.all()
    tech = Techniques.objects.all()

    tID = str(request.GET['tID'])
    tColor = str(request.GET['tColor'])

    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE DetectionChart_techniques SET techColor='" + tColor + "' WHERE techniqueId = '"+ tID +"'")
    db_connection.commit()

    all_dict = {'ttp': ttp , 'tac':tac, 'tech':tech }
    return render(request, 'base.html', all_dict)

def downloadToExcel(request):
    ConvertToExcel()
    return HttpResponseRedirect('static/downloads/attackv8.xlsx')

def updateDatabase(request):
    print("updating database")
    updateMITRE()
    updateMITRERepeats()
    return HttpResponseRedirect('/')

def resetDatabase(request):
    print("resetting database")
    flushDB()
    dataPullMITRE()
    attnavupdateRepeats()
    return HttpResponseRedirect('/')
