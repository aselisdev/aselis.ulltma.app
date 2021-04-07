# Generated by Django 3.1 on 2020-10-07 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0002_auto_20201007_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningstyle',
            name='style',
            field=models.CharField(choices=[('V', 'VISUAL'), ('A', 'AUDITORY'), ('MM', 'MULTIMODAL')], default='V', max_length=5),
        ),
    ]
