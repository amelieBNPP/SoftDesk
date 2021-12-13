# Generated by Django 3.2.9 on 2021-12-13 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_projects_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('to do', 'To do'), ('in progress', 'In progress'), ('done', 'Done')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[('bug', 'Bug'), ('feature', 'Feature'), ('improvement', 'Improvement')], max_length=128),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('iOS', 'iOS'), ('android', 'Android')], max_length=128),
        ),
    ]