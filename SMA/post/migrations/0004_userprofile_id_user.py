# Generated by Django 5.1.3 on 2024-12-31 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_followercount'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='id_user',
            field=models.IntegerField(default=0),
        ),
    ]
