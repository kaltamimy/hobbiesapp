# Generated by Django 3.2.8 on 2021-12-13 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_user_dob'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hobbies',
            new_name='Hobby',
        ),
    ]