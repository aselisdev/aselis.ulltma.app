# Generated by Django 3.1 on 2021-02-14 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0026_auto_20210205_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreports',
            name='posttestavg',
            field=models.FloatField(default=0),
        ),
    ]
