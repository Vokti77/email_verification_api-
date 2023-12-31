# Generated by Django 3.1.7 on 2023-08-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20230827_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothe',
            name='clothes_original',
        ),
        migrations.AddField(
            model_name='clothe',
            name='clothes_orginal',
            field=models.FileField(default=1, upload_to='clothes_orginal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clothe',
            name='clothes',
            field=models.FileField(default=5, upload_to='clothes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clothe',
            name='clothes_mask',
            field=models.FileField(upload_to='clothes_mask'),
        ),
    ]
