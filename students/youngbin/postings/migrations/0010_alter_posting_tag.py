# Generated by Django 4.0.4 on 2022-04-25 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0009_rename_tag_tag_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='tag',
            field=models.ManyToManyField(null=True, related_name='_postings', through='postings.Posting_Tag', to='postings.tag'),
        ),
    ]
