# Generated by Django 4.0.5 on 2022-08-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_remove_question_time_alter_answer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
