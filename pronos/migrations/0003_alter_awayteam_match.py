# Generated by Django 3.2.4 on 2021-06-26 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pronos', '0002_alter_awayteam_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awayteam',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayteams', to='pronos.match'),
        ),
    ]