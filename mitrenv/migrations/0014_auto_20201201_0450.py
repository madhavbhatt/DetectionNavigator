# Generated by Django 3.1.3 on 2020-12-01 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitrenv', '0013_techniques_techcolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniques',
            name='techColor',
            field=models.CharField(default='white', max_length=100, null=True),
        ),
    ]
