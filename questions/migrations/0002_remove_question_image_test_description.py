# Generated by Django 4.0.5 on 2022-10-17 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
