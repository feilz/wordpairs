# Generated by Django 2.2.6 on 2020-07-28 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordrelation',
            name='wordDistance',
        ),
        migrations.AddField(
            model_name='wordrelation',
            name='closeDistance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordrelation',
            name='longDistance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordrelation',
            name='mediumDistance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wordrelation',
            name='shortDistance',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='WordDistance',
        ),
    ]
