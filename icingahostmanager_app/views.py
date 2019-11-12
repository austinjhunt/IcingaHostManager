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
import os,fnmatch,csv,io, socket

from ipaddress import ip_address,ip_network

def isvalidIP(ip):
    octets=ip.split('.')
    if len(octets) != 4: return False
    try: return all(0 <= int(o) < 256 for o in octets)
    except ValueError: return False
import re
def isvalidAddress(addr): # can be either valid IP or valid FQDN
    failcond = len(addr) > 255 or addr[-1] == "." or len(addr) == 1 or " " in addr
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    successcond = all(allowed.match(x) for x in addr.split(".")) or isvalidIP(addr)
    return not failcond and successcond

class InvalidIPException(Exception):
    pass

def ajax(request):
    return request.is_ajax()

# for ajax requests, returning JSON to JS
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


# NOTE: When adding a new field for hosts, do the following:
# Add to MODAL_FIELDS here
# Add to available_fields list in index with description
# Add a column to the edit hosts table in hostmanager.html
# Increment the TOTALNUMFIELDS variable in main.js
# Recompress
# Add an input field for this field to the add single host form with input name prefixed by 'host'

MODAL_FIELDS = ['name', 'address', 'state', 'notes','num_cpus','os','env', 'network_zone', 'checks_to_execute', 'datacenter',
                        'cluster', 'process_names','disable_notifications',  'disable_wmi', 'disable_ssh', 'http_vhosts', 'ncpa']

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
class HostObj:
    def __init__(self,fields):
        for f in fields:
            setattr(self,f,None)


@csrf_exempt
def index(request):
    # Dont need to handle authentication. All authentication will be handled by Icinga application.
    # Just serve the home page.
    template = loader.get_template('hostmanager.html')
    # session variable to pass to and from confirmation page after new hosts are input
    request.session['successful_newhosts'] = []
    request.session['failed_newhosts'] = []

    context = {'page': 'index',
               'modal_fields': MODAL_FIELDS}
    # Need to provide available field names for anyone who wants to upload a csv of hosts
    available_fields = [
        AF("name", "Name of the host", 1),
        AF("address", "Address of the host; could be the same as the host's name", 1),
        AF("os","Operating system",1),
        AF("notes", "Notes about host",0),
        AF("network_zone","Which network zone does the host belong to? (e.g. Test, Production, Management, Development)",0),
        AF("checks_to_execute", "Comma-separated list of checks you wish to execute (shown in available checks table); be sure to wrap in double quotes",1),
        AF("process_names", "Names of processes you want to specifically check for if you include the is_process_running check in your checks_to_execute_field",0),
        AF("http_vhosts", "comma-separated list of virtual hosts running on the Host (e.g. the ServerName value of each VHost)",0),
        AF("num_cpus", "Number of CPUs on Host",0),
        AF("state", "Current state of Host (On/Off)",1),
        AF("env", "Environment in which Host lives (e.g. Echo, Drake, etc.)",0),
        AF("disable_notifications", "0 or 1 representing whether or not to disable notifications for this host; if not included, notifications will be enabled",0),
        AF("disable_wmi", "Only matters for Windows machines, will not affect Linux; 0 or 1 representing whether or not to disable WMI checks for Host; if not included, notifications will be enabled",0),
        AF("disable_ssh", "Only matters for Linux machines, will not affect Windows; 0 or 1 representing whether or not to disable SSH-based checks on Host; if not included, notifications will be enabled",0),
        AF("datacenter", "Name of datacenter to which the Host belongs",0),
        AF("cluster", "Name of cluster to which the Host belongs", 0),
        AF("ncpa", "Whether or not to use NCPA agent-based check", 0)
    ]
    context['available_fields'] = available_fields

    context['existing_hosts'] = Host.objects.all()
    # Merge the available checks from nagios path and customscriptspath
    try:
        available_checks = [f for f in os.listdir("/usr/local/nagios/libexec/") if fnmatch.fnmatch(f,"check*") or fnmatch.fnmatch(f,"is_proc*")] + \
                           [f for f in os.listdir("/etc/icinga2/scripts/custom_checks/") if fnmatch.fnmatch(f,"check*")]

        context['available_checks'] = available_checks
    except Exception as e:
        print(e)
        pass

    return HttpResponse(template.render(context,request))
@csrf_exempt
def ihm_logout(request):
    logout(request)
    #return HttpResponseRedirect("http://cofc.edu")
    return HttpResponseRedirect("https://login.microsoftonline.com/common/oauth2/logout")

# From Daniel, Oct 22 2019, if within 10.7.69.125-144 range, do not include in Icinga Host objects
# Check if in that range, add to failed_newhosts if true, specify why
# Helper methods for checking if in IP range:
# metatoaster on stackoverflow gives the following
# Convert IP into tuples of integers through comprehension expression
EXCLUDE_IP_RANGE = ('10.7.69.125','10.7.69.144')
EXCLUDE_IP_RANGE2 = ip_network('10.131.10.0/23')


def convert_ipv4(ip):
    return tuple(int(n) for n in ip.split('.'))

# Be sure to only pass valid IP addresses to this function
def check_ipv4_in(addr, start, end):
    return convert_ipv4(start) < convert_ipv4(addr) < convert_ipv4(end)

@csrf_exempt
def addsinglehost(request):
    if request.method == "POST":
        # Get form data
        template = loader.get_template('confirmation.html')
        try:
            # All inputs standardized with a prefix "host"
            fields_to_set = [k[4:] for k in request.POST.keys() if k != "checksTable_length"]
            host = HostObj(fields_to_set)
            for k in request.POST.keys():
                if k != "checksTable_length":
                    hostattr = k[4:]
                    postval = request.POST[k].strip()
                    # if POST value empty, set value to None for object
                    if postval == "":
                        print("Setting",hostattr,"to None")
                        setattr(host,hostattr,None)
                    elif postval == "0" or postval == "1":
                        postval = True if postval == "1" else False
                        setattr(host,hostattr,postval)
                    else: # not empty, not a boolean, just string value
                        print(request.POST[k],EXCLUDE_IP_RANGE)
                        if hostattr == "checks_to_execute":
                            setattr(host,hostattr,request.POST[k][1:])
                        elif hostattr == "address" and not isvalidAddress(request.POST[k]):
                            raise InvalidIPException("Invalid address: " + request.POST[k])
                        elif hostattr == "address" and isvalidIP(request.POST[k]) and check_ipv4_in(request.POST[k],*EXCLUDE_IP_RANGE):
                            raise InvalidIPException("Address",request.POST[k],"within IP Exclusion range",EXCLUDE_IP_RANGE)
                        elif hostattr == "address" and isvalidIP(request.POST[k]) and ip_address(request.POST[k]) in ip_network(EXCLUDE_IP_RANGE2):
                            raise InvalidIPException("Address", request.POST[k], "within IP Exclusion range",
                                                     EXCLUDE_IP_RANGE2)
                        else:
                            setattr(host,hostattr,request.POST[k])

            request.session['successful_newhosts'] = [json.dumps(host.__dict__)]
            columns = [el.capitalize() for el in host.__dict__.keys()]
            context = {'type': 'single success','successfulhostinfo':[host.__dict__],'successfulcolumns':columns,'failedcolumns':columns}
            print(host,columns)
        except Exception as e:
            print(e)
            setattr(host,"error",str(e))
            request.session['failed_newhosts'] = [json.dumps(host.__dict__)]
            columns = [el.capitalize() for el in host.__dict__.keys()]
            print(host,columns)
            context = {'type': 'single fail', 'exception': str(e),'failedhostinfo': [host.__dict__],'successfulcolumns':columns,'failedcolumns':columns}
        return HttpResponse(template.render(context,request))
    else: #only accept post requests
        return HttpResponseRedirect('/')

@csrf_exempt
def bulkuploadhosts(request):
    if request.method == "POST": # handle processing\
        template = loader.get_template("confirmation.html")
        try:
            csvupload = io.TextIOWrapper(request.FILES["hostsfile"].file,encoding=request.encoding)

            includesheader = True if request.POST.get('includesheader') == '1' else False

            # If this is true, assign the value of whatever field is marked with 'name' to the 'address' property of the
            # host being created
            nameresolve = True if request.POST.get('use_name_as_address','off') == 'on' else False

            fields_ordered = [el.strip() for el in request.POST['fields_ordered'].split(',')]
            # map the given fields to the columns of the input csv; create one host object per row

            lines = list(csv.reader(csvupload,quotechar='"',delimiter=',',skipinitialspace=True))
            lines = lines if not includesheader else lines[1:]
            successful_newhosts = []
            failed_newhosts = []
            for l in lines:
                # l is already a list
                newhost = HostObj(fields_ordered) # initialize all fields to None
                try:
                    successful_host = True # only keep true if you make it all the way past inner loop
                    for index,field in enumerate(fields_ordered):
                        value = l[index].strip()
                        # Dont process if empty input
                        if value == "":
                            print(field, "is empty")
                            setattr(newhost, field, None)

                        # Is this address column?
                        addresscolumn = (field == "address" or (nameresolve and field == "name"))

                        if not addresscolumn:
                            # Process the boolean fields
                            if value == "0" or value == "1" :
                                value = True if value == "1" else False
                                setattr(newhost, field, value)

                            # Process specifically checks_to_execute, remove leading ,
                            if field == "checks_to_execute":
                                setattr(newhost,field,value[1:])
                            # Process non boolean fields
                            else:
                                setattr(newhost, field,value)

                        # Specific handling for address; If this field is explicitly the address column or if this field is the name column to be used as address
                        if addresscolumn:
                            address = l[index]
                            print("Setting host",field,"to ",address)
                            setattr(newhost,"address",address)
                            if not isvalidAddress(l[index]):
                                successful_host = False

                    # Was this host created without problems?
                    if not successful_host:
                        setattr(newhost,"error","Invalid address: " + address)
                        failed_newhosts.append(newhost.__dict__)
                    else:
                        successful_newhosts.append(newhost.__dict__)
                except Exception as e:
                    newhost.error = e
                    failed_newhosts.append(newhost)
            request.session['successful_newhosts'] = [json.dumps(h) for h in successful_newhosts]
            request.session['failed_newhosts'] = [json.dumps(h) for h in failed_newhosts]

            successfulcolumns = [el.capitalize() for el in successful_newhosts[-1].keys()]
            failedcolumns = [el.capitalize() for el in failed_newhosts[-1].keys()]
            context = {
                'type': 'bulk success',
                'successfulhostinfo':successful_newhosts,
                'failedhostinfo':failed_newhosts,
                'successfulcolumns': successfulcolumns,
                'failedcolumns':failedcolumns
            }
        except Exception as e:
            context = {'type':'bulk fail','exception':str(e)}
        return HttpResponse(template.render(context,request))
    else:
        # only accept posts here
        return HttpResponseRedirect("/")


@csrf_exempt
def submit_successful_hosts(request):
    successful_hosts = request.session['successful_newhosts']
    # Each object in list is currently a JSON string. Need to use json.loads
    default_checks_to_execute = "ping4,"
    try:
        successful_hosts = [json.loads(s) for s in successful_hosts]
        for h in successful_hosts:
            # create a Database record for this host.
            print(h)

            if h.get('checks_to_execute','') is None:
                checks = default_checks_to_execute
            else:
                checks = default_checks_to_execute + h.get('checks_to_execute','')

            # FIXME: make this more modular, don't want to have to add a field to this every time a new field is considered. e.g. ncpa
            record = Host(name=h.get('name',None),
                          address=h.get('address',None),
                          state=h.get('state',None),
                          notes=h.get('notes',None),
                          num_cpus=h.get('num_cpus',1),
                          os=h.get('os',None),
                          env=h.get('env',"Echo"),
                          network_zone=h.get('network_zone',None),
                          checks_to_execute=checks,
                          datacenter=h.get('datacenter',None),
                          cluster=h.get('cluster',None),
                          process_names=h.get('process_names',None),
                          disable_notifications=h.get('disable_notifications',False),
                          disable_wmi=h.get('disable_wmi',False),
                          disable_ssh=h.get('disable_ssh',False),
                          http_vhosts=h.get('http_vhosts',None),
                          check_command=h.get('check_command','hostalive'),
                          zone=h.get('zone',"IZ-A"),
                          template_choice=h.get('template_choice',"DefaultHostTemplate"),
                          ncpa=h.get('use_ncpa',False)).save()

    except Exception as e:
        print(e)
    return HttpResponseRedirect("/")
@csrf_exempt
def edit_hosts(request):
    if request.method == "POST": # process
        try:
            hosts = request.POST.get('hosts',None)
            hosts = json.loads(hosts)
            print(hosts)
            for k in hosts:
                print("K = ",k)
                host_id = k.split("edithostsmodal_host_id_")[-1]
                print("Host id:",host_id)
                host = Host.objects.get(id=host_id)
                print(hosts[k])
                for k2 in hosts[k]:
                    print("Setting",k2,"to",hosts[k][k2])
                    setattr(host,k2, hosts[k][k2])
                host.save()


            data = {'res':'success'}
        except Exception as e:
            data = {'res':'fail','e':str(e)}
        return render_to_json_response(data)
@csrf_exempt
def delete_hosts(request):
    if request.method == "POST":
        try:
            print(request.POST)
            hostids_to_delete = json.loads(request.POST.get('hosts_to_delete'))
            for parseid in hostids_to_delete:
                id = parseid.split("deletehostsmodal_host_id_")[-1]
                Host.objects.get(id=id).delete()

            data = {'res':'success'}
        except:
            data = {'res':'fail'}

        return render_to_json_response(data)




@csrf_exempt
def filter_hosts_by_ip(request):
    if request.method == "POST":
        range_subnet = request.POST.get('range')
        ip_range = False
        subnet = False
        if "-" in range_subnet:
            begin = range_subnet.split("-")[0].strip()
            end = range_subnet.split("-")[-1].strip()
            ip_range = (begin,end)
            print("Ip range:",ip_range)
        elif "/" in range_subnet:
            subnet = ip_network(range_subnet.strip())
            print("Subnet:",subnet)
        # Get all hosts
        hosts = Host.objects.all()
        hostsinrange = []
        template = loader.get_template('hostmanager.html')
        try:
            for h in hosts:
                if isvalidIP(h.address.strip()):
                    addr = h.address.strip()
                    # Check if in range/subnet
                    if ip_range:
                        addr_in_ip_range = check_ipv4_in(addr,*ip_range)
                        if addr_in_ip_range:
                            print("Host",addr,"in IP range",ip_range)
                            hostsinrange.append(h)
                    elif subnet:
                        addr_in_subnet = ip_address(addr) in subnet
                        if addr_in_subnet:
                            hostsinrange.append(h)
                            print("Host",addr,"in subnet",subnet)

                else: # not a valid ip, but a hostname, get ip.
                    print(h.address,"not a valid IP")
                    try:
                        addr = socket.gethostbyname(h.address)
                        print("Address:",addr)
                        # Check if in range/subnet
                        if ip_range:
                            addr_in_ip_range = check_ipv4_in(addr, *ip_range)
                            if addr_in_ip_range:
                                print("Host",h.address,"in IP range",ip_range)
                                hostsinrange.append(h)
                        elif subnet:
                            addr_in_subnet = ip_address(addr) in subnet
                            if addr_in_subnet:
                                hostsinrange.append(h)
                                print("Host", h.address, "in subnet", subnet)
                    except:
                        # Don't worry about this host
                        continue
            context = {'existing_hosts':hostsinrange, 'range':request.POST.get('range'),'modal_fields':MODAL_FIELDS}
        except Exception as e:
            print(e)
            context = {'range':request.POST.get('range'),'existing_hosts': [],'modal_fields': MODAL_FIELDS}

        return HttpResponse(template.render(context,request))
        print(hostsinrange)


    else:
        return HttpResponseRedirect("/")

@csrf_exempt
def toggle_notifications_all_hosts(request):


