# Generated by Django 2.0 on 2018-11-12 14:50

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20181112_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='MSecond_Quest_Polygon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('level', models.IntegerField(default='0')),
                ('description', models.TextField()),
                ('picture', models.CharField(default='', max_length=100)),
                ('color', models.CharField(default='#ff7800', max_length=20)),
                ('geom', djgeojson.fields.PolygonField()),
            ],
        ),
        migrations.CreateModel(
            name='Second_Quest_Marker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('level', models.IntegerField(default='0')),
                ('description', models.TextField()),
                ('picture', models.ImageField(upload_to='')),
                ('icon', models.TextField(default='')),
                ('geom', djgeojson.fields.PointField()),
            ],
        ),
        migrations.RenameField(
            model_name='mushroomspot',
            old_name='num',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='point',
            old_name='num',
            new_name='level',
        ),
    ]