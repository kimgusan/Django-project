# Generated by Django 5.0.2 on 2024-03-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_rename_image_postfile_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
