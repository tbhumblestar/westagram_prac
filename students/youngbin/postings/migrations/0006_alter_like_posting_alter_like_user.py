# Generated by Django 4.0.4 on 2022-04-23 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('postings', '0005_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='postings.posting'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='users.user'),
        ),
    ]
