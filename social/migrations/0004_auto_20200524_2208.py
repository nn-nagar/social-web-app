# Generated by Django 3.0.6 on 2020-05-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20200524_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
