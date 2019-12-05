from django.db import models

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=60,default="",null=False)
    address = models.CharField(max_length=60,default="",null=False)
    state = models.CharField(max_length=60,default="On")
    notes = models.TextField(null=True)
    num_cpus = models.IntegerField(null=True)
    os = models.CharField(max_length=60,null=False,default="Red Hat/RHEL")
    env = models.CharField(max_length=60,null=False,default="Echo")
    network_zone = models.CharField(max_length=60,null=True)
    checks_to_execute = models.TextField(null=True)
    datacenter = models.CharField(max_length=60,null=True)
    cluster = models.CharField(max_length=60,null=True)
    process_names = models.TextField(null=True)
    disable_notifications = models.BooleanField(default=False)
    disable_wmi = models.BooleanField(default=False)
    disable_ssh = models.BooleanField(default=False)
    http_vhosts = models.TextField(null=True)
    check_command = models.CharField(max_length=60,default="hostalive",null=False)

    #FIXME: add input fields for each of these
    zone = models.CharField(max_length=10,default="IZ-A")
    template_choice = models.CharField(max_length=60,default="DefaultHostTemplate")

    # Transitioning to all ncpa checks for standardization. Uses an agent;
    # Use this as a custom var to determine if ncpa check should be used on host.
    ncpa = models.BooleanField(default=False)
