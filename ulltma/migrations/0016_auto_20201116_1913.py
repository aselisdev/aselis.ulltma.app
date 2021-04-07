# Generated by Django 3.1 on 2020-11-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0015_learningtool'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseskill',
            name='subject',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='baseskill',
            name='topic',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='baseskill',
            name='skill',
            field=models.CharField(default='', max_length=500),
        ),
    ]
