# Generated by Django 4.0.5 on 2022-08-18 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('accounts', '0005_alter_user_group_alter_userquestionscore_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='groups.group'),
        ),
    ]
