# Generated by Django 4.0.4 on 2022-07-23 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_user_maximum_earning_per_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='maximum_earning_per_day',
            field=models.FloatField(default=200),
        ),
    ]
