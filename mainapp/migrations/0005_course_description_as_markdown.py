# Generated by Django 4.1.2 on 2022-12-05 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_course_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description_as_markdown',
            field=models.BooleanField(default=False, verbose_name='Разметка Markdown'),
        ),
    ]
