# Generated by Django 3.2.4 on 2021-06-27 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pronos', '0010_auto_20210627_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awayteam',
            name='hometeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='pronos.hometeam'),
        ),
        migrations.AlterField(
            model_name='awayteam',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match', to='pronos.match'),
        ),
        migrations.AlterField(
            model_name='match',
            name='hometeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometeam', to='pronos.hometeam'),
        ),
    ]