# Generated by Django 4.0.4 on 2022-04-23 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0003_alter_comment_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='User',
            new_name='user',
        ),
    ]
