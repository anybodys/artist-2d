# Generated by Django 5.0.6 on 2024-09-08 21:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_create_first_generation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dna', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Art',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('public_link', models.URLField()),
                ('generation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.generation')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VotingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.art')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.votinguser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
