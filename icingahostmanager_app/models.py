from django.db import models

from dynamic_models.models import AbstractModelSchema, AbstractFieldSchema

class ModelSchema(AbstractModelSchema):
    pass

class FieldSchema(AbstractFieldSchema):
    pass

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

class Field(models.Model):
    default = models.BooleanField(default=False)
    field_name = models.CharField(max_length=60,null=False,primary_key=True)
    description = models.TextField(null=False)
    input_type = models.CharField(max_length=60,null=False,default="text") # front end input config
    # if input_type == select, you'll have FieldDropdownOption mapped to this object

    display_name = models.CharField(max_length=60, null=False)

    # Model (host attribute) configuration.
    # model attribute name will use field_name value

    # model attribute.null = allow null values or no?
    model_field_null = models.BooleanField(default=True,null=False)

    # when field is set for Host model, use ... field = models.model_field_type(...)
    # Options: charfield,TextField,BooleanField,IntegerField
    model_field_type = models.CharField(default="CharField",max_length=60,null=False)

    model_field_default_value = models.CharField(max_length=60,default="",null=False)
    #   ii) null Boolean (allow null values or no?)
    #   iii) default value



class FieldDropdownOption(models.Model):
    field = models.ForeignKey(Field,on_delete=models.CASCADE,null=False)
    option = models.CharField(max_length=60,default="Test Option", null=False)
