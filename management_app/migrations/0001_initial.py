# Generated by Django 5.1.4 on 2024-12-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=10)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('backlog', 'Backlog'), ('to_do', 'To Do'), ('in_progress', 'In Progress'), ('review', 'Review'), ('completed', 'Completed')], default='in_progress', max_length=15)),
            ],
        ),
    ]