# Generated by Django 2.2.2 on 2019-10-28 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icingahostmanager_app', '0011_host_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='template_choice',
            field=models.CharField(default='DefaultHostTemplate', max_length=60),
        ),
    ]