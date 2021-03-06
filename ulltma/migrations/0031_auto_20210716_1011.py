# Generated by Django 3.1 on 2021-07-16 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0030_learningtool_viability'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreports',
            name='style',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ulltma.learningstyle'),
        ),
        migrations.AlterField(
            model_name='learningtool',
            name='viability',
            field=models.CharField(choices=[('VB', 'VIABLE'), ('NVB', 'NOT VIABLE')], default='VB', max_length=25),
        ),
    ]
