# Generated by Django 3.2.4 on 2021-06-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronos', '0014_auto_20210629_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='point',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
