# Generated by Django 3.1.2 on 2020-12-07 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201107_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitedpeople',
            name='rooms',
            field=models.SmallIntegerField(default=0, verbose_name='房间数'),
        ),
    ]
