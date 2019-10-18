# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q, Count
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from random import *
# Create your views here.
class Break_Nested_Loop(Exception): pass
from django.template import loader
from .models import *
from .forms import *
import json
# DRY Utility Functions

import os,fnmatch,csv,io

def ajax(request):
    return request.is_ajax()

# for ajax requests, returning JSON to JS
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


# When user requests page, immediately invoke the microsoft authentication
# That will return with a POST to the successful_login(request) function.
# Only then, direct them to / where index will be called with request.user.is_authenticated being true.
# Right now, the "Microsoft" button on the /admin/ page triggers the Microsoft auth. Instead of passing the
# login url to the javascript, pass it to this file, and let index redirect to that url.

class AF:
    def __init__(self,n,d,r):
        self.name = n
        self.description = d
        self.required = True if r else False
class Host:
    def __index__(self,hostname,hostaddress,hoststate,hostnotes,hostnumcpus,hostenv,hostnetzone,hostos,hostchecks_to_execute,
                  hostprocess_names,hostdisable_notifications,hostdisable_wmi,hostdisable_ssh,hosthttp_vhosts,hostdatacenter,hostcluster):
        self.name = hostname
        self.address = hostaddress
        self.state = hoststate
        self.notes = hostnotes
        self.num_cpus = hostnumcpus
        self.environment = hostenv
        self.netzone = hostnetzone
        self.os = hostos
        self.checks_to_execute = hostchecks_to_execute
        self.process_names = hostprocess_names
        self.disable_notifications = hostdisable_notifications
        self.disable_wmi = hostdisable_wmi
        self.disable_ssh = hostdisable_ssh
        self.http_vhosts = hosthttp_vhosts
        self.datacenter = hostdatacenter
        self.cluster = hostcluster

@csrf_exempt
def index(request):
    # Dont need to handle authentication. All authentication will be handled by Icinga application.
    # Just serve the home page.
    template = loader.get_template('hostmanager.html')
    context = {'page': 'index'}
    # Need to provide available field names for anyone who wants to upload a csv of hosts
    available_fields = [
        AF("name", "Name of the host", 1),
        AF("address", "Address of the host; could be the same as the host's name", 1),
        AF("os","Operating system",1),
        AF("notes", "Notes about host",0),
        AF("netzone","Which network zone does the host belong to? (e.g. Test, Production, Management, Development)",0),
        AF("checks_to_execute", "Comma-separated list of checks you wish to execute (shown in available checks table); be sure to wrap in double quotes",1),
        AF("process_names", "Names of processes you want to specifically check for if you include the is_process_running check in your checks_to_execute_field",0),
        AF("http_vhosts", "comma-separated list of virtual hosts running on the Host (e.g. the ServerName value of each VHost)",0),
        AF("num_cpus", "Number of CPUs on Host",0),
        AF("state", "Current state of Host (On/Off)",1),
        AF("environment", "Environment in which Host lives (e.g. Echo, Drake, etc.)",0),
        AF("disable_notifications", "0 or 1 representing whether or not to disable notifications for this host; if not included, notifications will be enabled",0),
        AF("disable_wmi", "Only matters for Windows machines, will not affect Linux; 0 or 1 representing whether or not to disable WMI checks for Host; if not included, notifications will be enabled",0),
        AF("disable_ssh", "Only matters for Linux machines, will not affect Windows; 0 or 1 representing whether or not to disable SSH-based checks on Host; if not included, notifications will be enabled",0),
        AF("datacenter", "Name of datacenter to which the Host belongs",0),
        AF("cluster", "Name of cluster to which the Host belongs", 0)
    ]
    context['available_fields'] = available_fields
    # Merge the available checks from nagios path and customscriptspath
    try:
        # available_checks = [f for f in os.listdir("/usr/local/nagios/libexec/") if fnmatch.fnmatch(f,"check*") or fnmatch.fnmatch(f,"is_proc*")] + \
         #   [f for f in os.listdir("/etc/icinga2/scripts/custom_checks/") if fnmatch.fnmatch(f,"check*")]
        # context['available_checks'] = available_checks
        test_available_checks = [f for f in os.listdir("/Users/austinhunt/Desktop/")]
        context['available_checks'] = test_available_checks
    except Exception as e:
        print(e)
        pass

    return HttpResponse(template.render(context,request))
@csrf_exempt
def ihm_logout(request):
    logout(request)
    #return HttpResponseRedirect("http://cofc.edu")
    return HttpResponseRedirect("https://login.microsoftonline.com/common/oauth2/logout")
@csrf_exempt
def addsinglehost(request):
    if request.method == "POST":
        # Get form data

        template = loader.get_template('new_addition.html')
        try:
            hostname = request.POST['hostname'].strip()
            hostaddress = request.POST['hostaddress'].strip()
            hoststate = request.POST['hoststate'].strip()
            hostnotes = request.POST['hostnotes'].strip()
            hostnotes = None if hostnotes.strip() == "" else hostnotes
            hostnumcpus = request.POST['hostnumcpus']
            hostnumcpus = None if hostnumcpus.strip() == "" else hostnumcpus
            hostenv = request.POST['hostenv']
            hostnetzone = request.POST['hostnetzone']
            hostnetzone = None if hostnetzone == "0" else hostnetzone
            hostos = request.POST['hostos']
            hostchecks_to_execute = request.POST['checks_to_execute']
            printstr = """Host Name: {}\nHost Address:{}\nHost State:{}\nHost Notes:{}\nNumber of CPUs:{}\nHost Environment:{}\nHost Zone:{}\nHost OS:{}\nChecks to Execute:{}""".format(hostname,hostaddress,hoststate,hostnotes,hostnumcpus,hostenv,hostnetzone,hostos,hostchecks_to_execute)
            print(printstr)
            #Host(name=hostname,address=hostaddress,state=hoststate,notes=hostnotes,num_cpus=hostnumcpus,env=hostenv,network_zone=hostnetzone,
             #    os=hostos).save()
            # create dict, display new info as tabe
            hostobj = Host(hostname,hostaddress,hoststate,hostnotes,hostnumcpus,hostenv,hostnetzone,hostos,hostchecks_to_execute)
            context = {'type':'single success','hostinfo':[hostobj]}
        except:
            context = {'type': 'single fail'}
        return HttpResponse(template.render(context,request))
    else: #only accept post requests
        return HttpResponseRedirect('/')
@csrf_exempt
def bulkuploadhosts(request):
    if request.method == "POST": # handle processing
        print(request.POST)
        template = loader.get_template("new_addition.html")

        csvupload = io.TextIOWrapper(request.FILES["hostsfile"].file,encoding=request.encoding)

        includesheader = True if request.POST.get('includesheader','off') == 'on' else False
        fields_ordered = request.POST['fields_ordered'].split(',')
        # map the given fields to the columns of the input csv; create one host object per row

        lines = list(csv.reader(csvupload,quotechar='"',delimiter=',',skipinitialspace=True))
        lines = lines if not includesheader else lines[1:]
        print("all lines:",lines)
        newhosts = []
        for l in lines:
            # l is already a list
            newhost = Host()
            for index,field in enumerate(fields_ordered):
                setattr(newhost,field,l[index])
            newhosts.append(newhost)
        context = {
           'hostinfo': newhosts  # show all the hosts here
        }
        return HttpResponse(template.render(context,request))
    else:
        # only accept posts here
        return HttpResponseRedirect("/")