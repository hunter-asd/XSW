# Generated by Django 2.2.4 on 2020-07-06 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_auto_20200705_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='explog',
            old_name='context',
            new_name='content',
        ),
    ]
