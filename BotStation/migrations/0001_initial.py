# Generated by Django 3.1.3 on 2021-04-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempUserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=14)),
                ('last_incoming', models.CharField(default=None, max_length=10000)),
                ('last_outgoing', models.CharField(default=None, max_length=2000)),
                ('datatime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserClone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=200)),
                ('password', models.CharField(max_length=30)),
                ('contact_no', models.CharField(max_length=14)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]
