# Generated by Django 3.1 on 2021-09-24 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0034_skilltestquestion_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltestquestion',
            name='imgurl',
            field=models.CharField(max_length=10000),
        ),
    ]
