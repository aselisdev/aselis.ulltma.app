# Generated by Django 3.1 on 2020-10-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0003_auto_20201007_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningstyle',
            name='style',
            field=models.CharField(default='VISUAL', max_length=20),
        ),
    ]
