# Generated by Django 3.0.8 on 2020-10-05 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20201005_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='mess',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='mob',
            new_name='mobile',
        ),
    ]
