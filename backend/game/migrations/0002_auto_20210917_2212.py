# Generated by Django 3.2.6 on 2021-09-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='first_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='second_count',
            field=models.IntegerField(default=0),
        ),
    ]
