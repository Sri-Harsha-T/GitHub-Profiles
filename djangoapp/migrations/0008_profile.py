# Generated by Django 3.2.6 on 2021-09-17 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djangoapp', '0007_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.IntegerField(null=True)),
                ('timeupdated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'profile',
                'managed': False,
            },
        ),
    ]