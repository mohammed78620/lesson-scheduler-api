# Generated by Django 3.2.19 on 2023-07-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='lesson',
            field=models.CharField(choices=[('wrestling', 'Wrestling'), ('jui-jitsu', 'Jui-jitsu'), ('boxing', 'Boxing')], max_length=20),
        ),
    ]
