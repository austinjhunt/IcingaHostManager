# Generated by Django 2.2.2 on 2019-10-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icingahostmanager_app', '0007_auto_20191021_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='env',
            field=models.CharField(default='Echo', max_length=60, null=True),
        ),
    ]