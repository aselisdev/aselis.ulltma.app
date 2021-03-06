# Generated by Django 3.1 on 2020-10-23 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ulltma', '0006_auto_20201014_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='UserReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1pretestscore', models.IntegerField()),
                ('q2pretestscore', models.IntegerField()),
                ('q3pretestscore', models.IntegerField()),
                ('q1posttestscore', models.IntegerField()),
                ('q2posttestscore', models.IntegerField()),
                ('q3posttestscore', models.IntegerField()),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ulltma.baseskill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2000)),
                ('imgurl', models.CharField(max_length=300)),
                ('answer', models.CharField(max_length=300)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ulltma.baseskill')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2000)),
                ('imgurl', models.CharField(max_length=300)),
                ('first', models.CharField(max_length=300)),
                ('second', models.CharField(max_length=300)),
                ('third', models.CharField(max_length=300)),
                ('fourth', models.CharField(max_length=300)),
                ('answer', models.IntegerField()),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ulltma.baseskill')),
            ],
        ),
    ]
