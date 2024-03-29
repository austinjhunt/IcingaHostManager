# Generated by Django 2.2.2 on 2019-11-13 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('address', models.CharField(default='', max_length=60)),
                ('state', models.CharField(default='On', max_length=60)),
                ('notes', models.TextField(null=True)),
                ('num_cpus', models.IntegerField(null=True)),
                ('os', models.CharField(default='Red Hat/RHEL', max_length=60)),
                ('env', models.CharField(default='Echo', max_length=60)),
                ('network_zone', models.CharField(max_length=60, null=True)),
                ('checks_to_execute', models.TextField(null=True)),
                ('datacenter', models.CharField(max_length=60, null=True)),
                ('cluster', models.CharField(max_length=60, null=True)),
                ('process_names', models.TextField(null=True)),
                ('disable_notifications', models.BooleanField(default=False)),
                ('disable_wmi', models.BooleanField(default=False)),
                ('disable_ssh', models.BooleanField(default=False)),
                ('http_vhosts', models.TextField(null=True)),
                ('check_command', models.CharField(default='hostalive', max_length=60)),
                ('zone', models.CharField(default='IZ-A', max_length=10)),
                ('template_choice', models.CharField(default='DefaultHostTemplate', max_length=60)),
                ('ncpa', models.BooleanField(default=False)),
            ],
        ),
    ]
