# Generated by Django 5.0.6 on 2024-09-09 00:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_artist_art_votinguser_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='art',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='art',
            name='generation',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='art',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.CreateModel(
            name='NewArtist',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dna', models.TextField()),
                ('public_link', models.URLField()),
                ('generation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.generation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewVote',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.newartist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.votinguser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='Art',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
