# Generated by Django 3.1.3 on 2020-11-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitrenv', '0008_auto_20201125_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniques',
            name='techniqueId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='techniques',
            name='techniqueName',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
