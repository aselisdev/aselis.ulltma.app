# Generated by Django 3.1 on 2021-11-19 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulltma', '0043_auto_20211007_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilltestquestion',
            name='op10',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op10img',
            field=models.ImageField(default='-', upload_to='op10pics'),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op11',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op11img',
            field=models.ImageField(default='-', upload_to='op11pics'),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op12',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op12img',
            field=models.ImageField(default='-', upload_to='op12pics'),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op7',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op7img',
            field=models.ImageField(default='-', upload_to='op7pics'),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op8',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op8img',
            field=models.ImageField(default='-', upload_to='op8pics'),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op9',
            field=models.CharField(default='-', max_length=50000),
        ),
        migrations.AddField(
            model_name='skilltestquestion',
            name='op9img',
            field=models.ImageField(default='-', upload_to='op9pics'),
        ),
    ]
