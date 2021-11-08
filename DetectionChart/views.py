from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,Http404, HttpResponseRedirect
from attnav import *
from .models import *
from manageDB import *
from download import *
from update import *
from backupdb import *
import mysql.connector
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.clickjacking import *
from django.views.decorators.cache import never_cache


@login_required(login_url='/login/')
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

#@login_required(login_url='/admin/')
@login_required(login_url='/login/')
def detvalue(request):
    ttp = TTP.objects.all()
    tac = Tactic.objects.all()
    tech = Techniques.objects.all()

    tID = str(request.GET['tID'])
    tColor = str(request.GET['tColor'])

    tidreg1 = re.compile(r'T\d{4}')
    tidreg2 = re.compile(r'T\d{4}.\d{3}')

    if tidreg1.fullmatch(tID) or tidreg2.fullmatch(tID):
        db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
        db_cursor = db_connection.cursor()
        db_cursor.execute("""UPDATE DetectionChart_techniques SET techColor= %(tcolor)s WHERE techniqueId = %(tid)s""", {'tcolor': tColor, 'tid': tID})
        db_connection.commit()

    all_dict = {'ttp': ttp, 'tac': tac, 'tech': tech}
    return render(request, 'base.html', all_dict)

@login_required(login_url='/login/')
def downloadToExcel(request):
    ConvertToExcel()
    return HttpResponseRedirect('static/downloads/attackv8.xlsx')


@login_required(login_url='/login/')
def backupDatabase(request):
    print("Backing Up database")
    manualBackupDatabase()
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def updateDatabase(request):
    print("updating database")
    updateMITRE()
    updateMITRERepeats()
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def resetDatabase(request):
    print("resetting database")
    flushDB()
    dataPullMITRE()
    attnavupdateRepeats()
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def downloadOSXAtomicTests(request):
    return HttpResponseRedirect('static/atomictests/osx/osx-atomic-tests.tar.gz')


@login_required(login_url='/login/')
def downloadLinuxAtomicTests(request):
    return HttpResponseRedirect('static/atomictests/linux/LINUX-atomic_red_team_automated_test.py')


@xframe_options_deny
@never_cache
def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/")


