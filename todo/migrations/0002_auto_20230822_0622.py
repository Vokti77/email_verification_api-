# Generated by Django 3.1.7 on 2023-08-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]