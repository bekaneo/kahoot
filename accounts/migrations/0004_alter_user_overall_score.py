# Generated by Django 4.0.5 on 2022-08-18 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_overall_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='overall_score',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
