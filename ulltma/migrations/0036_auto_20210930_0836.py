# Generated by Django 3.1 on 2021-09-30 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0035_auto_20210924_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltestquestion',
            name='imgurl',
            field=models.CharField(default='-', max_length=10000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='op1',
            field=models.CharField(default='-', max_length=2000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='op2',
            field=models.CharField(default='-', max_length=2000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='op3',
            field=models.CharField(default='-', max_length=2000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='op4',
            field=models.CharField(default='-', max_length=2000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='op5',
            field=models.CharField(default='-', max_length=2000),
        ),
        migrations.AlterField(
            model_name='skilltestquestion',
            name='qtype',
            field=models.CharField(choices=[('shortanswer', 'shortanswer'), ('longanswer', 'longanswer'), ('multoptions', 'multoptions'), ('graph', 'graph'), ('numberline', 'numberline')], max_length=20),
        ),
    ]
