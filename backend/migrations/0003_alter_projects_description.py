# Generated by Django 3.2.9 on 2021-12-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20211206_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='description',
            field=models.CharField(blank=True, max_length=2048),
        ),
    ]
