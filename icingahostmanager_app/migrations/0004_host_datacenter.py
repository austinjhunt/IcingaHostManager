# Generated by Django 2.2.2 on 2019-10-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icingahostmanager_app', '0003_host_checks_to_execute'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='datacenter',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
