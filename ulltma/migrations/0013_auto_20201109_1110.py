# Generated by Django 3.1 on 2020-11-09 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0012_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepicture',
            name='pfp',
            field=models.ImageField(default='media/ulltma/pfp/default.png', upload_to='media/ulltma/pfp'),
        ),
    ]
