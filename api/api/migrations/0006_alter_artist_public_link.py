# Generated by Django 5.1.1 on 2024-09-15 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_newvote_artist_remove_newvote_user_artist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='public_link',
            field=models.URLField(null=True),
        ),
    ]
