# Generated by Django 2.0 on 2018-11-12 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0015_auto_20181112_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstquestpolygon',
            name='quest',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='map.Quest'),
        ),
    ]
