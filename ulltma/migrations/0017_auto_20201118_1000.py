# Generated by Django 3.1 on 2020-11-18 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0016_auto_20201116_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningtool',
            name='title',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='learningtool',
            name='url',
            field=models.CharField(default='', max_length=300),
        ),
    ]
