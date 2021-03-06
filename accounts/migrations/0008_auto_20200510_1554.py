# Generated by Django 2.2.2 on 2020-05-10 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200502_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='employee status'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='manager status'),
        ),
    ]
