# Generated by Django 5.0.6 on 2024-06-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_remove_hangmangames_date_played_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hangmangames',
            name='guesses_allowed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hangmangames',
            name='guesses_taken',
            field=models.IntegerField(default=0),
        ),
    ]
