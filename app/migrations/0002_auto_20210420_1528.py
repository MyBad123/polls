# Generated by Django 2.2.10 on 2021-04-20 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_start',
            field=models.DateTimeField(),
        ),
    ]
