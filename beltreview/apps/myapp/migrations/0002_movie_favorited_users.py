# Generated by Django 2.1.3 on 2018-11-16 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='favorited_users',
            field=models.ManyToManyField(related_name='favorited_movies', to='myapp.User'),
        ),
    ]
