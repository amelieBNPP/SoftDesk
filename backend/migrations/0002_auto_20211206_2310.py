# Generated by Django 3.2.9 on 2021-12-06 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('po', 'PO'), ('dev', 'Developer')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issues',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('in progress', 'In progress'), ('done', 'Done')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[('bug', 'Bug'), ('feature', 'Feature'), ('cosmetic', 'Cosmetic')], max_length=128),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('fullstack', 'Fullstack')], max_length=128),
        ),
    ]
